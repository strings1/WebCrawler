from flask import Flask, render_template, request, redirect, url_for
import threading
import os
from webcrawler_project.storage.persistance import load_json
from webcrawler_project.storage.persistance import save_json
from webcrawler_project.crawler.manager import CrawlManager
from webcrawler_project.crawler.downloader_thread import DownloaderThread
from webcrawler_project.index.direct_index import build_direct_index
from webcrawler_project.index.inverted_index import build_inverted_index
from webcrawler_project.utils.trie import Trie
from webcrawler_project.search.boolean_search import boolean_search


app = Flask(__name__)

crawl_thread = None
crawl_manager = None
is_crawling = False
loaded_indexes = {
    "direct_index": {},
    "inverted_index": {}
}

if os.path.exists("indexes/direct_index.json"):
    loaded_indexes["direct_index"] = load_json("indexes/direct_index.json")
if os.path.exists("indexes/inverted_index.json"):
    loaded_indexes["inverted_index"] = load_json("indexes/inverted_index.json")

def start_crawler(start_url, output_dir, thread_count, max_pages):
    global crawl_manager, is_crawling
    is_crawling = True
    crawl_manager = CrawlManager(max_pages)
    crawl_manager.add_url(start_url)
    os.makedirs(output_dir, exist_ok=True)

    threads = []
    for _ in range(thread_count):
        d = DownloaderThread(crawl_manager)
        t = threading.Thread(target=d.run)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    stop = Trie(); exc = Trie()
    for w in ["the", "and", "is", "to", "in"]: stop.insert(w)
    for w in ["python", "webcrawler", "2024"]: exc.insert(w)
    
    direct_index = build_direct_index(output_dir, stop, exc)
    inverted_index = build_inverted_index(direct_index)

    save_json(direct_index, "indexes/direct_index.json")
    save_json(inverted_index, "indexes/inverted_index.json")
    is_crawling = False

@app.route("/", methods=["GET", "POST"])
def index():
    global crawl_thread, is_crawling

    if request.method == "POST":
        start_url = request.form["start_url"]
        output_dir = request.form["output_dir"]
        max_pages = int(request.form["max_pages"])
        thread_count = int(request.form["thread_count"])

        if not is_crawling:
            crawl_thread = threading.Thread(
                target=start_crawler,
                args=(start_url, output_dir, thread_count, max_pages),
                daemon=True
            )
            crawl_thread.start()

        return redirect(url_for("index"))

    return render_template("index.html", is_crawling=is_crawling)


@app.route("/search")
def search():
    query = request.args.get("query", "")
    if not query or not loaded_indexes["inverted_index"]:
        return render_template("search_results.html", query=query, results=[])

    all_docs = set(loaded_indexes["direct_index"].keys())
    results = boolean_search(query, loaded_indexes["inverted_index"], all_docs)
    return render_template("search_results.html", query=query, results=sorted(results))

if __name__ == "__main__":
    app.run(debug=True)
