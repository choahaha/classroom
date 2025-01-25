##### 기본 정보 입력 #####
# Streamlit 패키지 추가
import streamlit as st
# OpenAI 패키기 추가
import openai
import pandas as pd

api_key = st.secrets["OPENAI_API_KEY"]

##### 기능 구현 함수 #####
def askGpt(prompt,apikey):
    client = openai.OpenAI(api_key = apikey)
    response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": prompt}])
    gptResponse = response.choices[0].message.content
    return gptResponse

def load_data(file_path):
    return pd.read_csv(file_path)

##### 메인 함수 #####
def main():
    st.set_page_config(page_title="과정중심평가 AI 제작툴")

    #메인공간
    st.header("😎 과정중심평가 AI 제작툴")
    st.markdown('---')

    # 데이터 불러오기
    try:
        data = load_data("data.csv")  # data.csv 파일이 존재해야 함
    except FileNotFoundError:
        st.error("data.csv 파일을 찾을 수 없습니다. 올바른 위치에 파일을 추가하세요.")
        return

    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox("학년군", ["3-4학년군", "5-6학년군"])
        subject = st.text_input("과목", placeholder=" ")
        content = st.text_input("학습 내용", placeholder=" ")
        
    with col2:  
        activity1 = st.text_input("활동1", placeholder=" ")
        activity2 = st.text_input("활동2", placeholder=" ")
        activity3 = st.text_input("활동3", placeholder=" ")

    if st.button("과정중심평가 생성"):
        # 조건에 맞는 데이터 필터링
        filtered_data = data[(data['학년군'] == grade) & (data['과목'] == subject)]
        
        if not filtered_data.empty:
            # 필터링된 데이터를 프롬프트에 포함
            csv_info = ""
            for _, row in filtered_data.iterrows():
                csv_info += f"- 평가 도구: {row['평가 도구']}, 평가 요소: {row['평가 요소']}\n"
        else:
            csv_info = "관련 데이터가 없습니다. 직접 생성해보세요!"

        # GPT에 전달할 프롬프트 생성
        prompt = f"""
        당신은 과정중심평가의 전문가인 교사입니다. 아래 내용을 참고해서 수업활동별 과정중심평가 내용을 제안하려고 합니다.
        과정중심평가방법에는 관찰, 구술, 토의토론, 서술형, 프로젝트, 실험실습, 포트폴리오, 관찰법, 자기평가, 동료평가 등이 있습니다.
        평가 기준은 '~한다.'로 끝나도록 서술합니다. 평가 기준의 예시는 다음과 같습니다.
        '주변 위치나 장소에 관해 쉽고 간단한 문장으로 설명할 수 있다.'
        '생활 속 동물을 활용 목적에 따라 분류하고, 돌보고, 기르는 과정을 실행한다.'

        아래는 학년군과 과목별 평가 요소 및 평가 도구의 참고 데이터입니다:
        {csv_info}

        입력된 내용을 기반으로 평가 요소, 평가 방법, 평가 기준을 추천해주세요:
        - 초등학교 학년군: {grade}
        - 과목: {subject}
        - 학습 내용: {content}
        - 활동1: {activity1}
        - 활동2: {activity2}
        - 활동3: {activity3}

        출력은 다음 형식으로 해주세요:
        - 활동1:
          - 평가 요소:
          - 평가 방법:
          - 평가 기준:
        """
        
        # GPT에 프롬프트 전달 및 응답 출력
        try:
            response = askGpt(prompt, api_key)  # <-- api_key까지 함께 전달
            st.info(response)
        except Exception as e:
            st.error(f"GPT 요청 중 오류가 발생했습니다: {e}")

if __name__ == '__main__':
    main()
