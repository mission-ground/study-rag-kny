import pdfplumber

def extract_text_from_pdf(pdf_path):
    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 텍스트 추출 (표 레이아웃을 어느 정도 유지함)
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
    return "\n\n".join(text_content)