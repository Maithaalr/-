
import streamlit as st
import pandas as pd

st.set_page_config(page_title="تحليل النواقص", layout="wide")
st.title("تحليل النواقص في بيانات الموظفين")

st.markdown("<div class='section-header'>يرجى تحميل بيانات الموظفين</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("ارفع الملف", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, header=0)
    selected_sheet = st.selectbox("اختر الجهة", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]

    excluded_departments = ['HC.نادي عجمان للفروسية', 'PD.الشرطة المحلية لإمارة عجمان', 'RC.الديوان الأميري']
    if 'الدائرة' in df.columns:
        df = df[~df['الدائرة'].isin(excluded_departments)]

    fields = [
        "نوع العقد", "اسم المشرف", "بريد المشرف", "الفئة الوظيفية",
        "نوع الوظيفة", "المجموعة الوظيفية الفرعية", "المجموعة الوظيفية الرئيسية",
        "مكان الميلاد", "الديانة", "الحالة الاجتماعية", "رقم الجواز",
        "تاريخ اصدار الجواز", "تاريخ إنتهاء الجواز", "مكان اصدار الجواز",
        "رقم الهوية", "تاريخ إنتهاء الهوية", "العنوان المنطقة", "العنوان امارة", "رقم الهاتف"
    ]

    st.success("تم تحميل البيانات بنجاح")
    tabs = st.tabs(fields)

    for i, field in enumerate(fields):
        with tabs[i]:
            st.subheader(f"نواقص في: {field}")

            if field in df.columns:
                missing_rows = df[df[field].isnull() | (df[field].astype(str).str.strip() == '')]
                total_rows = len(df)
                missing_count = len(missing_rows)
                missing_percent = (missing_count / total_rows) * 100

                st.write(f"عدد السجلات التي تحتوي على نقص: **{missing_count}** من أصل {total_rows}")
                st.write(f"نسبة النقص: **{missing_percent:.2f}%**")

                st.dataframe(missing_rows, use_container_width=True)

                csv = missing_rows.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label="تحميل البيانات الناقصة",
                    data=csv,
                    file_name=f"missing_{field.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning(f"⚠️ الحقل **{field}** غير موجود في البيانات.")
