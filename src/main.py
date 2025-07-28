import logging

import httpx
from mcp.server.fastmcp import FastMCP

from exceptions import HTTPServerError
from shared import Criteria, ProgrammingLanguage
from websites.posting import BulldogJob, GenericPostingWebsite

logging.basicConfig(filename="server.log", level=logging.INFO)

mcp = FastMCP()


async def fetch_page_content(page_url: str) -> str:
    async with httpx.AsyncClient() as c:
        response = await c.get(page_url)
        response.raise_for_status()
        return response.read().decode()


@mcp.tool()
async def get_offer_information(posting_url: str) -> str:
    try:
        website = BulldogJob()
        return str({"name": website.host, "headers": website.headers})
    except HTTPServerError as ex:
        logging.error("Unable to fetch offer", exc_info=ex)
        return "Unable to fetch page name"
    return website.website_host


@mcp.tool()
async def get_offers(
    programmingLanguage: ProgrammingLanguage, criteria: Criteria, limit: int = 50
) -> str:
    logging.info(
        f"Fetching offers for language: {programmingLanguage}, criteria: {criteria}"
    )
    try:
        website = BulldogJob()
        offers = await website.list_offers_for(programmingLanguage, criteria)
        list_of_offers = []
        for _ in range(limit):
            list_of_offers.append(str(next(offers)))
        logging.info(f"Found offers {len(list_of_offers)}")
        return "\n\n".join(list_of_offers) if list_of_offers else "No offers found"
    except HTTPServerError as ex:
        logging.error("Unable to fetch offer", exc_info=ex)
        return "Unable to fetch offer"


if __name__ == "__main__":
    logging.info("Starting server ...")
    mcp.run(transport="stdio")
