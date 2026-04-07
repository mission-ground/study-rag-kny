from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunks(text):
    # 정책 자료는 한 문단이 아주 길지 않으므로 
    # 청크 사이즈를 600~800 정도로 잡고 문맥 유지를 위해 100자 정도 겹침
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        # 정책 자료의 구분자들(줄바꿈, 불렛 포인트 등)을 고려한 설정
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks