import os
import re
import logging  # Add logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.element_assets import ElementAsset, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("element_indexer")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///element_assets.db")  # Ensure SQLite is used
logger.info(f"Using DATABASE_URL={DATABASE_URL}")  # Log the database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite-specific argument
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", "home/lotfikan/blogv3/templates/")
STATIC_DIR = os.getenv("STATIC_DIR", "home/lotfikan/blogv3/static/")

INDEX_FLAG_FILE = os.path.join(TEMPLATES_DIR, ".indexing_done")  # File to track indexing status

def extract_classes_and_ids(html_content):
    """Extract classes and IDs from HTML content."""
    classes = re.findall(r'class="([^"]+)"', html_content)
    ids = re.findall(r'id="([^"]+)"', html_content)
    elements = set()
    for cls in classes:
        elements.update(f".{c.strip()}" for c in cls.split())
    elements.update(f"#{id.strip()}" for id in ids)
    return elements

def find_css_block(element, css_content):
    """Find the CSS block for a given element."""
    pattern = re.compile(rf"{re.escape(element)}\s*{{.*?}}", re.DOTALL)
    match = pattern.search(css_content)
    return match.group(0) if match else None

def find_js_snippets(element, js_content):
    """Find JS snippets referencing the element."""
    pattern = re.compile(rf"(document\.querySelector|document\.getElementById|['\"]{re.escape(element)}['\"]).*?;", re.DOTALL)
    return pattern.findall(js_content)

def index_elements():
    """Index elements from templates and static files."""
    if os.path.exists(INDEX_FLAG_FILE):
        logger.info("Indexing already completed. Skipping indexing process.")
        return

    session = Session()
    try:
        logger.info("Starting indexing process...")
        logger.info(f"Traversing templates directory: {TEMPLATES_DIR}")
        for root, _, files in os.walk(TEMPLATES_DIR):
            logger.info(f"Current directory: {root}")  # Log the current directory
            for file in files:
                if not file.endswith(".html"):
                    continue
                template_path = os.path.join(root, file)
                logger.info(f"Indexing template: {template_path}")  # Log the template being indexed
                with open(template_path, "r") as f:
                    html_content = f.read()

                elements = extract_classes_and_ids(html_content)
                logger.info(f"Found {len(elements)} elements in {template_path}")

                for element in elements:
                    css_block = None
                    js_snippets = []

                    # Search CSS files
                    for css_root, _, css_files in os.walk(STATIC_DIR):
                        for css_file in css_files:
                            if not css_file.endswith(".css"):
                                continue
                            with open(os.path.join(css_root, css_file), "r") as css_f:
                                css_content = css_f.read()
                                css_block = find_css_block(element, css_content)
                                if css_block:
                                    logger.info(f"CSS block found for {element} in {css_file}")
                                    break
                        if css_block:
                            break

                    # Search JS files
                    for js_root, _, js_files in os.walk(STATIC_DIR):
                        for js_file in js_files:
                            if not js_file.endswith(".js"):
                                continue
                            with open(os.path.join(js_root, js_file), "r") as js_f:
                                js_content = js_f.read()
                                snippets = find_js_snippets(element, js_content)
                                if snippets:
                                    logger.info(f"JS snippets found for {element} in {js_file}")
                                js_snippets.extend(snippets)

                    # Avoid duplicates
                    existing_entry = session.query(ElementAsset).filter_by(html_element=element).first()
                    if existing_entry:
                        logger.info(f"Skipping duplicate entry for {element}")
                        continue

                    # Insert into database
                    asset = ElementAsset(
                        html_element=element,
                        css_block=css_block,
                        js_snippets="\n".join(js_snippets),
                        template_file=template_path
                    )
                    session.add(asset)
                    logger.info(f"Inserted {element} into the database")

        session.commit()
        logger.info("Indexing process completed successfully.")

        # Create the flag file to indicate indexing is done
        with open(INDEX_FLAG_FILE, "w") as flag_file:
            flag_file.write("Indexing completed.")
    except Exception as e:
        logger.error(f"Error during indexing: {e}")
    finally:
        session.close()
