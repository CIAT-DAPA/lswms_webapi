import os
from urllib.parse import quote
from flask import request
from flask_restful import Resource
from mongoengine import Q
from ormWP import AdvisoryPdf, AdvisoryTypeEnum

# Carpeta física donde están los PDFs
PDF_DIR = os.getenv("PDF_DIR", r"D:\2025\data")

# 🔒 Forzar siempre que las URLs apunten al servidor de estáticos en localhost:4000/pdfs/
PDF_BASE_URL = os.getenv("PDF_BASE_URL", "http://localhost:4000/pdfs/")

def _ensure_trailing_slash(u: str) -> str:
    return u if u.endswith("/") else u + "/"

class AdvisoryPdfIndex(Resource):
    def __init__(self):
        super().__init__()

    def _base_url(self) -> str:
        # Forzamos origen a PDF_BASE_URL (por defecto http://localhost:4000/pdfs/)
        return _ensure_trailing_slash(PDF_BASE_URL)

    def get(self):
        """
        List available Advisory PDFs grouped by type
        ---
        description: Scan the filesystem folder for PDFs and return MongoDB metadata (name, description, download URL) for those filenames found, grouped by advisory type.
        tags:
          - Advisory PDFs
        responses:
          200:
            description: Grouped advisory PDFs
            schema:
              id: AdvisoryPdfGrouped
              properties:
                seasonal:
                  type: array
                  items:
                    $ref: "#/definitions/AdvisoryPdfItem"
                subseasonal:
                  type: array
                  items:
                    $ref: "#/definitions/AdvisoryPdfItem"
        definitions:
          AdvisoryPdfItem:
            type: object
            properties:
              filename:
                type: string
                description: Physical PDF file name
              name:
                type: string
                description: Human readable title
              description:
                type: string
                description: PDF description
              url:
                type: string
                description: Public download URL
        """
        # 1) Listar PDFs del filesystem
        try:
            filenames = [
                entry.name
                for entry in os.scandir(PDF_DIR)
                if entry.is_file() and entry.name.lower().endswith(".pdf")
            ]
        except FileNotFoundError:
            return {"seasonal": [], "subseasonal": []}, 200

        if not filenames:
            return {"seasonal": [], "subseasonal": []}, 200

        # 2) Traer solo los que existen en DB por filename
        docs = AdvisoryPdf.objects(filename__in=filenames)

        base_url = self._base_url()
        seasonal = []
        subseasonal = []

        # 3) Mapear a payload y agrupar (robusto si type es Enum o str)
        for doc in docs:
            raw_type = getattr(doc.type, "value", doc.type)
            if isinstance(raw_type, str):
                type_key = raw_type.lower()
            else:
                # Por si viniera como AdvisoryTypeEnum.SEASONAL -> "SEASONAL" -> "seasonal"
                type_key = str(raw_type).split(".")[-1].lower()

            item = {
                "filename": doc.filename,
                "name": doc.name,
                "description": doc.description or "",
                "url": base_url + quote(doc.filename),
            }

            if type_key == "seasonal":
                seasonal.append(item)
            elif type_key == "subseasonal":
                subseasonal.append(item)
            # otros tipos se ignoran

        # 4) Orden opcional (por name)
        seasonal.sort(key=lambda x: x["name"].lower())
        subseasonal.sort(key=lambda x: x["name"].lower())

        return {"seasonal": seasonal, "subseasonal": subseasonal}, 200
