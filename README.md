# WebCrawler

WebCrawler is a multi-threaded web crawler and search engine. It downloads and indexes web pages, supporting both boolean and vectorial search over the crawled content. The project features a Flask web interface for configuring crawl parameters, monitoring progress, and searching the indexed data with pagination support.

## Features

- Multi-threaded web crawling
- Configurable crawl parameters (start URL, output directory, max pages, thread count)
- Boolean and vectorial search over crawled content
- Flask web interface for configuration and search
- Index persistence (direct and inverted indexes)

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:strings1/WebCrawler.git
   cd WebCrawler/WebCrawler
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Flask Web App

To start the Flask web interface, run:

```bash
python -m webcrawler_project.web.app
```

The app will start in debug mode and be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage

1. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
2. Configure the crawler parameters (start URL, output directory, max pages, thread count)
3. Start the crawl and monitor progress
4. Use the search interface to query the indexed data

## Project Structure

- `webcrawler_project/` - Main source code
- `webcrawler_project/web/app.py` - Flask web application
- `requirements.txt` - Python dependencies
- `tests/` - Unit tests
- `docs/` - Sphinx documentation

## License

MIT License

---

*Developed by Darie Alexandru*