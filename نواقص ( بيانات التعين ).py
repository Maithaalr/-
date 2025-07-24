import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="تحليل النواقص", layout="wide")
st.title("تحليل النواقص في بيانات الموظفين")

uploaded_file = st.file_uploader("ارفع ملف الموظفين (Excel أو CSV)", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # الحقول المطلوبة
    fields = [
        "نوع العقد", "اسم المشرف", "بريد المشرف", "الفئة الوظيفية",
        "نوع الوظيفة", "المجموعة الوظيفية الفرعية", "المجموعة الوظيفية الرئيسية"
    ]

    st.success("تم تحميل البيانات بنجاح")

    tabs = st.tabs(fields)

    for i, field in enumerate(fields):
        with tabs[i]:
            st.subheader(f"نواقص في: {field}")

            # استخراج الصفوف التي فيها نقص
            missing_rows = df[df[field].isnull() | (df[field].astype(str).str.strip() == '')]
            total_rows = len(df)
            missing_count = len(missing_rows)
            missing_percent = (missing_count / total_rows) * 100

            st.write(f"عدد السجلات التي تحتوي على نقص: **{missing_count}** من أصل {total_rows}")
            st.write(f"نسبة النقص: **{missing_percent:.2f}%**")

            st.dataframe(missing_rows, use_container_width=True)

            # تحميل ملف
            file_name = f"missing_{field.replace(' ', '_')}.csv"
            csv = missing_rows.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="تحميل البيانات الناقصة",
                data=csv,
                file_name=file_name,
                mime="text/csv"
            )

