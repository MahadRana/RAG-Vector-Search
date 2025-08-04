from src.rag_project.data_collection.raw_docs import load_html_page
from src.rag_project.data_collection.create_chunks import make_chunk_records
from src.rag_project.data_collection.create_chunks import chunk_text
from chromadb import PersistentClient
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE
from src.logger import logging
from src.exception import CustomException
import sys

client = PersistentClient(
    path = './chroma_db',
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collection = client.get_or_create_collection(name='RAG_Vector')

def data_pipeline(url_lst):
    try:
        logging.info("=" * 40)
        logging.info("STARTING DATA PIPELINE")
        logging.info("=" * 40)

        for url in url_lst:
            raw_text = load_html_page(url)
            records = make_chunk_records(chunks=chunk_text(text=raw_text, id=url), url=url)
            del raw_text
            for record in records:
                collection.add(
                    ids = [record['id']],
                    documents = [record['text']],
                    metadatas = [record['metadata']]
                )
            del records
        # Pipeline end header
        logging.info("=" * 40)
        logging.info("DATA PIPELINE COMPLETE")
        logging.info("=" * 40)

    except Exception as e:
        raise CustomException(e,sys)

if __name__ == "__main__":
    article_urls = [
        "https://www.howtogeek.com/260248/how-to-make-windows-troubleshoot-your-pc-problems-for-you/",
        "https://www.howtogeek.com/troubleshoot-windows-command-prompt/",
        "https://www.howtogeek.com/222730/how-to-find-out-why-your-windows-pc-crashed-or-froze/",
        "https://www.lifewire.com/run-diagnostics-on-windows-5214801",
        "https://www.boostitco.com/blog/the-ultimate-guide-to-running-diagnostics-on-windows-10/",
        "https://windowsforum.com/threads/mastering-windows-11-troubleshooting-common-issues-and-solutions.351561/",
        "https://m.majorgeeks.com/content/page/how_to_use_the_microsoft_support_diagnostic_tool_system_diagnostic_report.html",
        "https://www.lifewire.com/fix-a-computer-that-shows-no-sign-of-power-2624442",
        "https://www.lifewire.com/how-to-fix-a-computer-that-wont-turn-on-2624450",
        "https://www.lifewire.com/fix-when-laptop-wont-turn-on-5120787",
        "https://www.lifewire.com/how-to-manually-test-a-power-supply-with-a-multimeter-2626158",
        "https://www.lifewire.com/what-does-reseat-mean-2625987",
        "https://www.howtogeek.com/757556/what-is-a-cpu-or-gpu-bottleneck-in-pc-gaming-and-how-to-fix-it/",
        "https://www.howtogeek.com/853523/gpu-fans-not-spinning/",
        "https://www.howtogeek.com/cpu-or-gpu-bottleneck-how-to-tell-and-which-is-worse/",
        "https://helpdeskgeek.com/see-how-much-your-cpu-bottlenecks-your-gpu-before-you-buy-it/",
        "https://www.lifewire.com/fix-disk-usage-windows-10-4583918",
        "https://www.lifewire.com/fix-stopping-freezing-and-reboot-issues-during-the-post-2624441",
        "https://superuser.com/questions/1282334/how-do-i-diagnose-a-computer-that-shows-no-signs-of-life-besides-a-lit-periphera",
        "https://onsitego.com/blog/laptop-fan-not-working-fix/",
        "https://learn.microsoft.com/en-us/answers/questions/3781818/random-black-screen-crash-during-gaming",
        "https://www.ifixit.com/Answers/View/206319/Monitor%2Bno%2Bsignal%2Bafter%2Bstart%2Bup",
        "https://www.bleepingcomputer.com/forums/t/684970/computer-is-absolutely-dead-no-signs-of-life-when-hitting-power-button/",
        "https://www.lifewire.com/why-restarting-fixes-computer-problems-8733211",
        "https://www.lifewire.com/fix-common-windows-11-issues-8780752",
    ]
    logging.info(f"Pre-ingest count: {collection.count()}")
    data_pipeline(article_urls)
    logging.info(f"Post-ingest count: {collection.count()}")