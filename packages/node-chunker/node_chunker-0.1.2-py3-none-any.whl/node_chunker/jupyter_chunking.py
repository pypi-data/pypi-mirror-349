import json
import logging
import os
import tempfile
from typing import Optional

from markitdown import MarkItDown

from .document_chunking import BaseDocumentChunker, TOCNode
from .md_chunking import MarkdownTOCChunker

# Get logger for this module
logger = logging.getLogger(__name__)


class JupyterNotebookTOCChunker(BaseDocumentChunker):
    """
    A document chunker that converts Jupyter Notebooks to Markdown using MarkItDown
    and then creates a hierarchical tree of nodes based on Markdown headings.
    """

    def __init__(self, notebook_path: str, source_display_name: str):
        """
        Initialize the chunker with the path to the Jupyter Notebook.

        Args:
            notebook_path: Path to the .ipynb file or JSON content
            source_display_name: The original name of the source
        """
        super().__init__(
            source_path=notebook_path, source_display_name=source_display_name
        )
        self.markdown_content: Optional[str] = None
        self._document_loaded = False

    def load_document(self) -> None:
        """Load the Jupyter notebook and convert it to Markdown using MarkItDown."""
        md_converter = MarkItDown(enable_plugins=False)
        temp_file_path = None

        try:
            # Check if source_path is a file path or JSON content
            if os.path.isfile(self.source_path):
                # If it's a file path, use it directly
                result = md_converter.convert(self.source_path)
                self.markdown_content = result.text_content
            else:
                # Assume it's JSON content, save to temp file first
                try:
                    notebook_content = json.loads(self.source_path)
                    with tempfile.NamedTemporaryFile(
                        mode="w", delete=False, suffix=".ipynb", encoding="utf-8"
                    ) as tmp_file:
                        json.dump(notebook_content, tmp_file)
                        temp_file_path = tmp_file.name

                    # Convert the temp file to markdown
                    result = md_converter.convert(temp_file_path)
                    self.markdown_content = result.text_content
                except json.JSONDecodeError:
                    logger.error("Source is neither a valid file path nor valid JSON content")
                    raise

            self._document_loaded = True

        except Exception as e:
            logger.error(f"Error converting Jupyter notebook to Markdown: {e}")
            raise
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def build_toc_tree(self) -> TOCNode:
        """
        Build a tree structure from the converted Markdown content.

        Returns:
            The root node of the TOC tree
        """
        if not self._document_loaded:
            self.load_document()

        if self.markdown_content is None:
            logger.error("Markdown content is not available after load_document.")
            # Return a basic root node if conversion failed
            self.root_node = TOCNode(
                title="Notebook Root", page_num=0, level=0, content=""
            )
            return self.root_node

        # Use MarkdownTOCChunker to process the converted content
        md_chunker = MarkdownTOCChunker(
            markdown_text=self.markdown_content,
            source_display_name=self.source_display_name,
        )
        self.root_node = md_chunker.build_toc_tree()

        return self.root_node

    def close(self) -> None:
        """Clean up resources"""
        self.markdown_content = None
        self._document_loaded = False
