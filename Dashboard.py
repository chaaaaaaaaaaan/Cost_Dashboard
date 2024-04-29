import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Data load
def load_data():

    data = pd.read_csv("cost_kyonggi_univ.csv", encoding="utf-8")
    data.fillna(0, inplace=True)
    #data.rename(columns={'서비스':'Date'}, inplace=True)

    return data.loc[0], data.rename(columns={'서비스':'Date'}).loc[1:] #total / month

#월별 클라우드 비용
def get_montly_cost_bar_chart(monthly):

    fig = px.bar(monthly, x="Date", y="총 비용($)", template=st.session_state.template)#color='index')
    fig.add_trace(go.Scatter(x=monthly["Date"], y=monthly["총 비용($)"],  ))
    fig.update_layout(showlegend=False, xaxis=dict(tickformat="%B %Y" ,dtick="M1"))
    st.plotly_chart(fig, use_container_width=True)

    return

#월별 인스턴스 비용
def get_instance_pie_chart(monthly):

    
    option = st.selectbox(
        '비용 확인할 월을 선택하세요',
        monthly["Date"]
    )
    mode = st.radio(label="Chart 선택", options=["pie", "bar"], horizontal=True)

    selected_data = monthly[monthly['Date'] == option]
    data = selected_data.drop(columns=['Date', '총 비용($)'])
    data = data.melt(var_name='서비스', value_name='비용')

    # 0 이상의 비용을 가진 서비스만 필터링
    data = data[data['비용'] > 0]

    if mode=="pie":
        # 파이 차트 생성
        fig = px.pie(data, values='비용', names='서비스', template=st.session_state.template)
        fig.update_traces(textposition='inside', textfont=dict(color="white"))
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)

    else:    
        #상위 10개 서비스 차트
        fig = px.bar(data.sort_values(by="비용",ascending=False).head(10), x='서비스',y='비용',color='서비스', template=st.session_state.template)
        st.plotly_chart(fig, use_container_width=True)

    return 

#인스턴스별 비용
def get_instance_bar_chart(total, monthly):
    
    services = monthly.columns[1:]
    for s in services:
        if total[s]==0: list(services).remove(s)
        
    #option
    #st.sidebar.text("인스턴스별 비용")
    option = st.selectbox(
        '비용 확인 할 서비스를 선택하세요',
        services
    )
    #st.sidebar.markdown("---")
    fig = px.bar(monthly, x="Date", y=option, template=st.session_state.template)
    fig.update_layout(showlegend=False, xaxis=dict(tickformat="%B %Y" ,dtick="M1"))
    st.plotly_chart(fig, use_container_width=True)
    return

def main():

    st.set_page_config(layout="wide")
    st.title("클라우드 서비스 비용")
    st.markdown("---")
    
    #사이드바
    with st.sidebar:

        # #태그 선택
        # tag_list = ["경기대","숙명여대","가천대"]
        # tag = st.selectbox(
        #     'Tag를 선택하세요',
        #     sorted(tag_list)
        # )
        
        #템플릿
        templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
        st.session_state.template = st.selectbox(
            '템플릿을 선택하세요',
            sorted(templates),
            index=2 #plotly
        )
        
        
    total, monthly = load_data()

    #레이아웃
    #Row1
    col1, col2, col3 = st.columns(3)
    with col1:
        #st.metric("당월 비용", "100 $", delta="1.5 $") 
        st.metric("당월 비용", "{:,.2f} $".format(monthly.loc[2,"총 비용($)"]), delta="{:,.2f}".format(monthly.loc[2,"총 비용($)"]-monthly.loc[1,"총 비용($)"]) )
    with col2:
        st.metric("평균 비용", "{:,.2f} $".format(monthly["총 비용($)"].mean()))

    with col3:
        pass

    st.markdown("---")

    #Row2
    col1, col2 = st.columns(2)
    with col1:
        st.text("클라우드 비용")
        get_montly_cost_bar_chart(monthly)
        pass
    
    with col2:
        st.text("월별 인스턴스 비용")
        get_instance_pie_chart(monthly)
        st.text("인스턴스별 비용")
        get_instance_bar_chart(total, monthly)

if __name__=="__main__":
    main()

