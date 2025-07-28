
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
        "تاريخ اصدار الجواز", "تاريخ إنتهاء الجواز", "جهة اصدار الجواز",
        "رقم الهوية", "تاريخ انتهاء الهوية", "العنوان المنطقة", "العنوان الامارة", "رقم الهاتف" , "المستوى التعليمي" , "هل المؤهل متوافق للوظيفة"
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

    # -------------------- Emirati-specific Section -------------------- #
    st.markdown("### 🔎 تحليل نواقص حقول خاصة للمواطنين (Emirati فقط)")

    emirati_df = df[df['الجنسية'].str.strip().str.lower() == "emirati"]
    emirati_fields = ["رقم خلاصة القيد" , "رقم البلدة", "رقم الأسرة", "الرقم الموحد"]

    for field in emirati_fields:
        st.subheader(f"نواقص في: {field} (Emirati فقط)")
        if field in emirati_df.columns:
            missing_rows = emirati_df[emirati_df[field].isnull() | (emirati_df[field].astype(str).str.strip() == '')]
            total_rows = len(emirati_df)
            missing_count = len(missing_rows)
            missing_percent = (missing_count / total_rows) * 100

            st.write(f"عدد السجلات التي تحتوي على نقص: **{missing_count}** من أصل {total_rows}")
            st.write(f"نسبة النقص: **{missing_percent:.2f}%**")

            st.dataframe(missing_rows, use_container_width=True)

            csv = missing_rows.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label=f"تحميل البيانات الناقصة ({field})",
                data=csv,
                file_name=f"missing_emirati_{field.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"⚠️ الحقل **{field}** غير موجود في البيانات.")


    # -------------------- تبويب عدد الأبناء -------------------- #
    st.markdown("### 👨‍👩‍👧‍👦 تحليل عدد الأبناء إذا الحالة الاجتماعية ليست Single")

    if "الحالة الاجتماعية" in df.columns and "عدد الأبناء" in df.columns:
        filtered_df = df[df["الحالة الاجتماعية"].str.strip().str.lower() != "single"]

        missing_children_rows = filtered_df[
            filtered_df["عدد الأبناء"].isnull() | (filtered_df["عدد الأبناء"].astype(str).str.strip() == "")
        ]

        total_rows = len(filtered_df)
        missing_count = len(missing_children_rows)
        missing_percent = (missing_count / total_rows) * 100 if total_rows else 0

        st.write(f"عدد الموظفين غير Single: **{total_rows}**")
        st.write(f"عدد السجلات التي لا تحتوي على عدد الأبناء: **{missing_count}**")
        st.write(f"نسبة النقص: **{missing_percent:.2f}%**")

        st.dataframe(missing_children_rows, use_container_width=True)

        csv = missing_children_rows.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="تحميل البيانات الناقصة (عدد الأبناء)",
            data=csv,
            file_name="missing_children_count.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ الحقول 'الحالة الاجتماعية' أو 'عدد الأبناء' غير موجودة.")


    # -------------------- تبويب: تحليل بيانات الكفالة للوافدين -------------------- #
    st.markdown("### 👤 تحليل بيانات الكفالة للوافدين (مع استثناء جنسيات الخليج)")

    sponsor_fields = ["الكفيل", "رقم الأقامة", "تاريخ اصدار اللإقامة", "تاريخ انتهاء اللإقامة"]
    excluded_gulf_nationalities = ["Emirati", "Omani", "Bahraini", "Saudi"]

    if "الجنسية" in df.columns:
        # استبعاد الجنسيات الخليجية
        df_foreign = df[~df["الجنسية"].isin(excluded_gulf_nationalities)].copy()

        for field in sponsor_fields:
            if field in df_foreign.columns:
                st.subheader(f"🔍 تحليل النواقص في: {field}")

                missing_rows = df_foreign[df_foreign[field].isnull() | (df_foreign[field].astype(str).str.strip() == "")]
                total_rows = len(df_foreign)
                missing_count = len(missing_rows)
                missing_percent = (missing_count / total_rows) * 100 if total_rows else 0

                st.write(f"عدد الوافدين: **{total_rows}**")
                st.write(f"عدد السجلات التي لا تحتوي على **{field}**: **{missing_count}**")
                st.write(f"نسبة النقص: **{missing_percent:.2f}%**")

                st.dataframe(missing_rows, use_container_width=True)

                csv = missing_rows.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label=f"تحميل البيانات الناقصة ({field})",
                    data=csv,
                    file_name=f"missing_{field.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning(f"⚠️ العمود '{field}' غير موجود في البيانات.")
    else:
        st.warning("⚠️ لا يوجد عمود للجنسية في الملف.")

