import contextlib
import logging
import os
from collections.abc import AsyncIterator

import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

# ---------------------------------------------------------------------------
# Weather helpers
# ---------------------------------------------------------------------------
OPENWEATHER_URL = "http://gfeljm.tianqiapi.com/api"
DEFAULT_UNITS = "metric"  # use Celsius by default
DEFAULT_LANG = "zh_cn"  # Chinese descriptions


async def fetch_weather(city: str,api_key: str) -> dict[str, str]:
    """Call OpenWeather API and return a simplified weather dict.

    Raises:
        httpx.HTTPStatusError: if the response has a non-2xx status.
    """
    params = {
        "version":"v61",
        "appid":"78875865",
        "appsecret": "vnm0pO1N",
        "city": city,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPENWEATHER_URL, params=params)
        r.raise_for_status()
        data = r.json()
    
    tianqi=data.get("wea")
    maxtem=data.get('tem1')
    mintem=data.get('tem2')
    humidity = data.get("humidity")
    win_speed=data.get("win_speed")
    return {
        "city": city,
        "weather": f"{tianqi}",
        "maxtemp": f"{maxtem}°C",
        "mintemp": f"{mintem}°C",
        "humidity": f"{humidity}",
        "win_speed":f"{win_speed}",
    }


@click.command()
@click.option("--port", default=3000, help="Port to listen on for HTTP")
@click.option(
    "--api-key",
    envvar="OPENWEATHER_API_KEY",
    required=True,
    help="OpenWeather API key (or set OPENWEATHER_API_KEY env var)",
)
@click.option(
    "--log-level",
    default="INFO",
    help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=False,
    help="Enable JSON responses instead of SSE streams",
)
def main(port: int, api_key: str, log_level: str, json_response: bool) -> int:
    """Run an MCP weather server using Streamable HTTP transport."""

    # ---------------------- Configure logging ----------------------
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("weather-server")

    # ---------------------- Create MCP Server ----------------------
    app = Server("mcp-streamable-http-weather")

    # ---------------------- Tool implementation -------------------
    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        """Handle the 'get-weather' tool call."""
        ctx = app.request_context
        city = arguments.get("location")
        if not city:
            raise ValueError("'location' is required in arguments")

        # Send an initial log message so the client sees streaming early.
        await ctx.session.send_log_message(
            level="info",
            data=f"Fetching weather for {city}…",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        try:
            weather = await fetch_weather(city, api_key)
        except Exception as err:
            # Stream the error to the client and re-raise so MCP returns error.
            await ctx.session.send_log_message(
                level="error",
                data=str(err),
                logger="weather",
                related_request_id=ctx.request_id,
            )
            raise

        # Stream a success notification (optional)
        await ctx.session.send_log_message(
            level="info",
            data="Weather data fetched successfully!",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        # Compose human-readable summary for the final return value.
        summary = (
            f"{weather['city']}：{weather['weather']}，最低温度 {weather['mintemp']}，"
            f"最高温度 {weather['maxtemp']}，湿度 {weather['humidity']},风速{weather['win_speed']}。"
        )

        return [
            types.TextContent(type="text", text=summary),
        ]

    # ---------------------- Tool registry -------------------------
    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """Expose available tools to the LLM."""
        return [
            types.Tool(
                name="get-weather",
                description="查询指定城市的实时天气",
                inputSchema={
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市的中文名称，不包含市，如青岛",
                        }
                    },
                },
            )
        ]

    # ---------------------- Session manager -----------------------
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,  # 无状态；不保存历史事件
        json_response=json_response,
        stateless=True,
    )

    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:  # noqa: D401,E501
        await session_manager.handle_request(scope, receive, send)

    # ---------------------- Lifespan Management --------------------
    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        async with session_manager.run():
            logger.info("Weather MCP server started! 🚀")
            try:
                yield
            finally:
                logger.info("Weather MCP server shutting down…")

    # ---------------------- ASGI app + Uvicorn ---------------------
    starlette_app = Starlette(
        debug=False,
        routes=[Mount("/mcp", app=handle_streamable_http)],
        lifespan=lifespan,
    )

    import uvicorn

    uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    return 0


if __name__ == "__main__":
    main()