import logging
from datetime import datetime
from uuid import UUID

from mcp.server.fastmcp import FastMCP

from db import get_db
from exceptions import HTTPServerError
from models import PostingModel
from repositories import BaseDBRepository
from schema import Posting
from shared import Criteria, ProgrammingLanguage
from websites.posting import BulldogJob

logging.basicConfig(filename="server.log", level=logging.INFO)

mcp = FastMCP()


@mcp.resource(
    "resumem://postings/",
    name="List of postings for selected seniority",
    mime_type="text/plain",
)
async def list_saved_postings() -> list:
    with get_db() as session:
        repo = BaseDBRepository(session, Posting)
        saved_postings = repo.get_all()
        logging.info(f"{saved_postings} - fetched")
        return [PostingModel.model_validate(obj) for obj in saved_postings]


@mcp.tool()
async def save_posting(name: str, posting_url: str) -> None:
    with get_db() as session:
        repo = BaseDBRepository(session, Posting)
        post = Posting(
            name=name,
            url=posting_url,
            tags="hi,bye,ad,ai",
            seniority="sennior",
            scraped_on=datetime.now(),
        )
        repo.add_one(post)


@mcp.tool()
async def delete_posting(item_id: int | UUID) -> None:
    with get_db() as session:
        repo = BaseDBRepository(session, Posting)
        repo.delete_one(item_id)


@mcp.tool()
async def get_offer_information(posting_url: str) -> str:
    try:
        website = BulldogJob()
        return str({"name": website.host, "headers": website.headers})
    except HTTPServerError as ex:
        logging.error("Unable to fetch offer", exc_info=ex)
        return "Unable to fetch page name"


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
