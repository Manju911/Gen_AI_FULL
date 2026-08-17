import asyncio
import os

from app.services.vector_store import add_document


async def main():

    knowledge_dir = "knowledge"

    files = os.listdir(
        knowledge_dir
    )

    for filename in files:

        if not filename.endswith(".txt"):
            continue

        path = os.path.join(
            knowledge_dir,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        document_id = filename.replace(
            ".txt",
            ""
        )

        await add_document(
            document_id,
            text
        )

        print(
            f"Indexed: {filename}"
        )


if __name__ == "__main__":

    asyncio.run(main())