import streamlit as st
import openai

##### GPT 호출 함수 #####
def askGpt(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

##### 메인 함수 #####
def main():
    st.set_page_config(page_title="과정중심평가 AI 제작툴")

    st.header("😎 과정중심평가 AI 제작툴")
    st.markdown("---")

    # 사용자 입력 받기
    grade = st.selectbox("학년군", ["3-4학년군", "5-6학년군"])
    subject = st.text_input("과목", placeholder="과목을 입력하세요.")
    content = st.text_input("학습 내용", placeholder="학습 내용을 입력하세요.")
    activity1 = st.text_input("활동1", placeholder="활동 1을 입력하세요.")
    activity2 = st.text_input("활동2", placeholder="활동 2를 입력하세요.")
    activity3 = st.text_input("활동3", placeholder="활동 3을 입력하세요.")

    if st.button("과정중심평가 생성"):
        # Streamlit Secrets에서 API 키 가져오기
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]  # API 키 가져오기

            # GPT에 전달할 프롬프트 작성
            prompt = f"""
            당신은 과정중심평가의 전문가인 교사입니다. 아래 내용을 참고해서 수업활동별 과정중심평가 내용을 제안하려고 합니다.

            - 초등학교 학년군: {grade}
            - 과목: {subject}
            - 학습 내용: {content}
            - 활동1: {activity1}
            - 활동2: {activity2}
            - 활동3: {activity3}

            출력은 다음과 같은 형식으로 작성하세요:
            - 활동1:
              - 평가 요소:
              - 평가 방법:
              - 평가 기준:
            """

            try:
                # API 키를 함께 전달하여 GPT 요청
                response = askGpt(prompt, api_key)
                st.info(response)
            except Exception as e:
                st.error(f"GPT 요청 중 오류가 발생했습니다: {e}")
        else:
            st.error("OpenAI API 키가 설정되지 않았습니다. Streamlit Secrets에서 설정해 주세요.")

if __name__ == "__main__":
    main()
