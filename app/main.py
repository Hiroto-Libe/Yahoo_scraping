from flask import Flask, jsonify, render_template, request

from . import api_client, config
from .csv_writer import write_csv
from .logger import log_event

app = Flask(__name__)


def _extract_items(payload):
    if isinstance(payload, dict):
        if "hits" in payload and isinstance(payload["hits"], list):
            return payload["hits"]
        if "ResultSet" in payload:
            result = payload["ResultSet"]
            hits = result.get("0", {}).get("Result", [])
            if isinstance(hits, list):
                return hits
    return []


def _extract_categories(payload):
    categories = []
    if not isinstance(payload, dict):
        return categories

    if "categories" in payload:
        cat_list = payload.get("categories", {}).get("category", [])
        if isinstance(cat_list, dict):
            cat_list = [cat_list]
        for cat in cat_list:
            categories.append({
                "id": cat.get("id") or cat.get("categoryId"),
                "name": cat.get("name"),
            })
        return categories

    if "ResultSet" in payload:
        result = payload.get("ResultSet", {}).get("0", {}).get("Result", [])
        if isinstance(result, dict):
            result = [result]
        for cat in result:
            categories.append({
                "id": cat.get("Id") or cat.get("id"),
                "name": cat.get("Name") or cat.get("name"),
            })
    return categories


@app.route("/")
def index():
    return render_template("index.html", results=[], message=None, csv_path=None)


@app.route("/categories")
def categories():
    if not config.APP_ID:
        return jsonify({"error": "YAHOO_APP_ID is not set"}), 400
    payload = api_client.get_categories()
    data = _extract_categories(payload)
    return jsonify({"categories": data})


@app.route("/search", methods=["POST"])
def search():
    if not config.APP_ID:
        return render_template("index.html", results=[], message="YAHOO_APP_ID is not set", csv_path=None)

    query = request.form.get("query", "").strip()
    category_id = request.form.get("category_id", "").strip()

    if not query or not category_id:
        return render_template("index.html", results=[], message="キーワードとカテゴリを入力してください", csv_path=None)

    try:
        payload = api_client.search_items(query=query, category_id=category_id)
        items = _extract_items(payload)
        csv_path = write_csv(items)
        log_event("INFO", "search_success", query=query, category_id=category_id, items=len(items))
        message = f"{len(items)}件取得しました。CSV: {csv_path}"
        return render_template("index.html", results=items, message=message, csv_path=csv_path)
    except Exception as exc:
        log_event("ERROR", "search_failed", query=query, category_id=category_id, error=str(exc))
        return render_template("index.html", results=[], message="取得に失敗しました", csv_path=None)


if __name__ == "__main__":
    app.run(debug=True)
