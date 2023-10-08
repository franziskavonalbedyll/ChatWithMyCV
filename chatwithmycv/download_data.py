"""Download CV explanations from Azure Blob Storage."""
import streamlit as st
from azure.storage.blob import BlobServiceClient


def download() -> None:
    """Download CV explanations from Azure Blob Storage."""
    blob_service_client = BlobServiceClient(
        account_url=st.secrets["ACCOUNT_SAS_URL"]
    )

    blob_client = blob_service_client.get_blob_client(
        container="cvdata", blob="cv_explanations.txt"
    )
    with open("../data/cv_explanations.txt", "wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())
