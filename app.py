import streamlit as st
import pandas as pd
from datetime import datetime
import html
import random


# -------------------------------------------------
# Sayfa ayarları
# -------------------------------------------------
st.set_page_config(
    page_title="Mizaç ve Karakter Özellikleri Değerlendirme",
    page_icon="🧠",
    layout="wide"
)


# -------------------------------------------------
# Ölçek maddeleri
# Katılımcıya alt boyut başlıkları gösterilmez.
# Alt boyut bilgisi yalnızca puanlama için arka planda kullanılır.
# -------------------------------------------------
SCALE_ITEMS = [
    {
        "dimension": "Yenilik Arayışı",
        "item": "Keşfetmekten heyecan duyarım."
    },
    {
        "dimension": "Yenilik Arayışı",
        "item": "Hızlı karar veririm."
    },
    {
        "dimension": "Yenilik Arayışı",
        "item": "Savurganım."
    },
    {
        "dimension": "Yenilik Arayışı",
        "item": "Düzensiz olduğumu düşünürüm."
    },

    {
        "dimension": "Zarardan Kaçınma",
        "item": "Endişeli ve karamsar olduğumu düşünürüm."
    },
    {
        "dimension": "Zarardan Kaçınma",
        "item": "Belirsizlikten korkarım."
    },
    {
        "dimension": "Zarardan Kaçınma",
        "item": "Yabancılardan çekinirim."
    },
    {
        "dimension": "Zarardan Kaçınma",
        "item": "Çabuk yorulurum."
    },

    {
        "dimension": "Ödül Bağımlılığı",
        "item": "Duygusal olduğumu düşünürüm."
    },
    {
        "dimension": "Ödül Bağımlılığı",
        "item": "Kolay bağlanırım."
    },
    {
        "dimension": "Ödül Bağımlılığı",
        "item": "Başka insanlara bağımlı bir yapım vardır."
    },

    {
        "dimension": "Sebat Etme",
        "item": "Mükemmeliyetçiyim."
    },
    {
        "dimension": "Sebat Etme",
        "item": "Amacıma ulaşmak için sınırları zorlarım."
    },
    {
        "dimension": "Sebat Etme",
        "item": "Kolay vazgeçmem."
    },
    {
        "dimension": "Sebat Etme",
        "item": "Sebat ederim."
    },

    {
        "dimension": "Kendi Kendini Yönetme",
        "item": "Sorumluluk alırım."
    },
    {
        "dimension": "Kendi Kendini Yönetme",
        "item": "Amaçlarımı kendim belirlerim."
    },
    {
        "dimension": "Kendi Kendini Yönetme",
        "item": "Becerikli olduğumu düşünürüm."
    },
    {
        "dimension": "Kendi Kendini Yönetme",
        "item": "Kendimi olduğum gibi kabullenirim."
    },
    {
        "dimension": "Kendi Kendini Yönetme",
        "item": "Değişikliklere kolay adapte olurum."
    },

    {
        "dimension": "İşbirliği Yapma",
        "item": "Başkalarını olduğu gibi kabullenirim."
    },
    {
        "dimension": "İşbirliği Yapma",
        "item": "Empati kurarım."
    },
    {
        "dimension": "İşbirliği Yapma",
        "item": "Yardım severim."
    },
    {
        "dimension": "İşbirliği Yapma",
        "item": "Acıma duygum vardır."
    },
    {
        "dimension": "İşbirliği Yapma",
        "item": "Temiz kalpli ve vicdanlıyım."
    },

    {
        "dimension": "Kendi Kendini Aşma",
        "item": "Yaptığım işe kendimi kaptırırım."
    },
    {
        "dimension": "Kendi Kendini Aşma",
        "item": "Çevremdeki insanları bir parçam olarak görürüm."
    },
    {
        "dimension": "Kendi Kendini Aşma",
        "item": "Hayatta manevi bir gücün yarattığı mükemmel bir düzen olduğuna inanırım."
    }
]


DIMENSION_ORDER = [
    "Yenilik Arayışı",
    "Zarardan Kaçınma",
    "Ödül Bağımlılığı",
    "Sebat Etme",
    "Kendi Kendini Yönetme",
    "İşbirliği Yapma",
    "Kendi Kendini Aşma"
]


DIMENSION_DESCRIPTIONS = {
    "Yenilik Arayışı": "Yüksek puan; keşfetmeye açıklık, yenilikten heyecan duyma, hızlı karar verme ve hareketlilik eğilimini gösterir.",
    "Zarardan Kaçınma": "Yüksek puan; kaygı, temkinlilik, belirsizlikten rahatsız olma, çekingenlik ve kolay yorulma eğilimine işaret eder.",
    "Ödül Bağımlılığı": "Yüksek puan; duygusallık, sosyal bağlara önem verme ve başkalarından etkilenme eğilimini gösterir.",
    "Sebat Etme": "Yüksek puan; kararlılık, hedefe bağlılık, kolay vazgeçmeme ve çabayı sürdürme eğilimini gösterir.",
    "Kendi Kendini Yönetme": "Yüksek puan; sorumluluk alma, amaç belirleme, kendini kabul etme, beceriklilik ve uyum sağlama düzeyinin yüksek olduğunu gösterir.",
    "İşbirliği Yapma": "Yüksek puan; empati, yardımseverlik, vicdanlılık, başkalarını kabullenme ve sosyal uyum eğilimini gösterir.",
    "Kendi Kendini Aşma": "Yüksek puan; kişinin kendini yaptığı işe kaptırması, çevresiyle bütünlük hissetmesi ve manevi anlam arayışıyla ilişkilidir."
}


# -------------------------------------------------
# Session state
# -------------------------------------------------
if "shuffled_items" not in st.session_state:
    st.session_state.shuffled_items = SCALE_ITEMS.copy()
    random.shuffle(st.session_state.shuffled_items)


# -------------------------------------------------
# Yardımcı fonksiyonlar
# -------------------------------------------------
def classify_score(percent):
    if percent <= 33:
        return "Düşük"
    elif percent <= 66:
        return "Orta"
    return "Yüksek"


def create_results(answers):
    results = []

    for dimension in DIMENSION_ORDER:
        dimension_items = [
            item for item in SCALE_ITEMS
            if item["dimension"] == dimension
        ]

        raw_score = 0

        for original_index, scale_item in enumerate(SCALE_ITEMS):
            if scale_item["dimension"] == dimension:
                raw_score += answers.get(original_index, 0)

        max_score = len(dimension_items)
        percent_score = round((raw_score / max_score) * 100, 2)
        level = classify_score(percent_score)

        results.append({
            "Alt Boyut": dimension,
            "Ham Puan": raw_score,
            "Maksimum Puan": max_score,
            "Yüzde Puanı": percent_score,
            "Düzey": level,
            "Yorum": DIMENSION_DESCRIPTIONS[dimension]
        })

    return pd.DataFrame(results)


def create_html_report(name, surname, df):
    full_name = f"{name} {surname}".strip()
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    rows = ""
    for _, row in df.iterrows():
        rows += f"""
        <tr>
            <td>{html.escape(str(row['Alt Boyut']))}</td>
            <td>{row['Ham Puan']} / {row['Maksimum Puan']}</td>
            <td>%{row['Yüzde Puanı']}</td>
            <td><strong>{html.escape(str(row['Düzey']))}</strong></td>
            <td>{html.escape(str(row['Yorum']))}</td>
        </tr>
        """

    report = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Mizaç ve Karakter Özellikleri Raporu</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #222;
                line-height: 1.6;
            }}
            h1 {{
                color: #243b53;
                border-bottom: 3px solid #bcccdc;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #334e68;
                margin-top: 30px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #d9e2ec;
                padding: 10px;
                vertical-align: top;
                text-align: left;
            }}
            th {{
                background-color: #f0f4f8;
            }}
            .info-box {{
                background-color: #f0f4f8;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
            }}
            .note {{
                margin-top: 30px;
                padding: 15px;
                background-color: #fffbea;
                border-left: 5px solid #f0b429;
            }}
        </style>
    </head>
    <body>
        <h1>Mizaç ve Karakter Özellikleri Değerlendirme Raporu</h1>

        <div class="info-box">
            <p><strong>Katılımcı:</strong> {html.escape(full_name)}</p>
            <p><strong>Rapor Tarihi:</strong> {date_str}</p>
        </div>

        <h2>Değerlendirme Yöntemi</h2>
        <p>
            Bu değerlendirmede her “Evet” yanıtı 1 puan, her “Hayır” yanıtı 0 puan olarak kabul edilmiştir.
            Ölçek maddeleri katılımcıya karışık sırada ve alt boyut başlıkları gösterilmeden sunulmuştur.
            Her madde arka planda ait olduğu alt boyuta göre puanlanmıştır.
        </p>

        <p>
            Her alt boyuta ait maddeler toplanmış ve ilgili alt boyutun ham puanı elde edilmiştir.
            Alt boyutlarda madde sayıları farklı olduğu için puanlar yüzdelik değere dönüştürülmüştür.
            Yüzde puanları 0–33 arası düşük, 34–66 arası orta, 67–100 arası yüksek düzey olarak yorumlanmıştır.
        </p>

        <h2>Sonuçlar</h2>
        <table>
            <thead>
                <tr>
                    <th>Alt Boyut</th>
                    <th>Puan</th>
                    <th>Yüzde</th>
                    <th>Düzey</th>
                    <th>Yorum</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <div class="note">
            <strong>Not:</strong> Bu kısa form klinik tanı koymak amacıyla kullanılmamalıdır.
            Sonuçlar yalnızca araştırma kapsamında betimleyici kişilik özelliği değerlendirmesi olarak yorumlanmalıdır.
            Bilimsel çalışmalarda kullanılması durumunda ölçeğin geçerlik ve güvenirlik analizlerinin ayrıca yapılması önerilir.
        </div>
    </body>
    </html>
    """

    return report


def create_text_report(name, surname, df):
    full_name = f"{name} {surname}".strip()
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    report = f"""
MİZAÇ VE KARAKTER ÖZELLİKLERİ DEĞERLENDİRME RAPORU

Katılımcı: {full_name}
Rapor Tarihi: {date_str}

DEĞERLENDİRME YÖNTEMİ
Her “Evet” yanıtı 1 puan, her “Hayır” yanıtı 0 puan olarak kodlanmıştır.
Ölçek maddeleri katılımcıya karışık sırada ve alt boyut başlıkları gösterilmeden sunulmuştur.
Her madde arka planda ait olduğu alt boyuta göre puanlanmıştır.
Her alt boyuta ait maddeler toplanarak ham puan elde edilmiştir.
Madde sayıları farklı olduğu için ham puanlar yüzdelik puana dönüştürülmüştür.
0–33 düşük, 34–66 orta, 67–100 yüksek düzey olarak yorumlanmıştır.

SONUÇLAR
"""

    for _, row in df.iterrows():
        report += f"""
{row['Alt Boyut']}
Puan: {row['Ham Puan']} / {row['Maksimum Puan']}
Yüzde Puanı: %{row['Yüzde Puanı']}
Düzey: {row['Düzey']}
Yorum: {row['Yorum']}
"""

    report += """
NOT
Bu kısa form klinik tanı koymak amacıyla kullanılmamalıdır.
Sonuçlar yalnızca araştırma kapsamında betimleyici kişilik özelliği değerlendirmesi olarak yorumlanmalıdır.
Bilimsel çalışmalarda kullanılması durumunda ölçeğin geçerlik ve güvenirlik analizlerinin ayrıca yapılması önerilir.
"""

    return report


# -------------------------------------------------
# Arayüz
# -------------------------------------------------
st.title("🧠 Mizaç ve Karakter Özellikleri Değerlendirme Formu")

st.markdown("""
Bu uygulama, katılımcının mizaç ve karakter özelliklerini kısa form üzerinden değerlendirmek için hazırlanmıştır.

Lütfen aşağıdaki maddeleri dikkatle okuyunuz ve size en uygun gelen seçeneği işaretleyiniz.  
Maddeler karışık sırada sunulmaktadır. Değerlendirme sonunda kişisel bir rapor oluşturulacaktır.
""")

with st.expander("ℹ️ Puanlama hakkında bilgi"):
    st.markdown("""
    - **Evet = 1 puan**
    - **Hayır = 0 puan**
    - Maddeler katılımcıya karışık sırada gösterilir.
    - Alt boyut başlıkları form ekranında gösterilmez.
    - Her madde arka planda ait olduğu alt boyuta göre puanlanır.
    - Sonuçlar yüzde puana dönüştürülür.
    - **0–33:** Düşük  
    - **34–66:** Orta  
    - **67–100:** Yüksek  
    """)

st.divider()


# -------------------------------------------------
# Katılımcı bilgileri
# -------------------------------------------------
st.subheader("I. Katılımcı Bilgileri")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Adınız", placeholder="Örn. Ayşe")

with col2:
    surname = st.text_input("Soyadınız", placeholder="Örn. Yılmaz")


st.divider()


# -------------------------------------------------
# Form
# -------------------------------------------------
st.subheader("II. Değerlendirme Maddeleri")

answers = {}

with st.form("personality_form"):
    for display_number, scale_item in enumerate(st.session_state.shuffled_items, start=1):
        original_index = SCALE_ITEMS.index(scale_item)

        response = st.radio(
            label=f"{display_number}. {scale_item['item']}",
            options=["Seçiniz", "Evet", "Hayır"],
            index=0,
            horizontal=True,
            key=f"item_{original_index}"
        )

        if response == "Evet":
            answers[original_index] = 1
        elif response == "Hayır":
            answers[original_index] = 0
        else:
            answers[original_index] = None

    submitted = st.form_submit_button("📊 Değerlendirmeyi Tamamla")


# -------------------------------------------------
# Sonuçlar
# -------------------------------------------------
if submitted:
    if not name.strip() or not surname.strip():
        st.error("Lütfen katılımcının adını ve soyadını giriniz.")

    elif any(value is None for value in answers.values()):
        st.error("Lütfen tüm maddeleri işaretleyiniz. Boş madde bırakılmamalıdır.")

    else:
        numeric_answers = {
            key: value for key, value in answers.items()
            if value is not None
        }

        result_df = create_results(numeric_answers)

        st.success("Değerlendirme başarıyla tamamlandı.")

        full_name = f"{name.strip()} {surname.strip()}"
        st.subheader(f"📌 {full_name} için Değerlendirme Sonuçları")

        # Özet metrikler
        average_score = round(result_df["Yüzde Puanı"].mean(), 2)
        highest_dimension = result_df.sort_values("Yüzde Puanı", ascending=False).iloc[0]
        lowest_dimension = result_df.sort_values("Yüzde Puanı", ascending=True).iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Ortalama Yüzde Puanı", f"%{average_score}")

        with col2:
            st.metric(
                "En Yüksek Boyut",
                highest_dimension["Alt Boyut"],
                f"%{highest_dimension['Yüzde Puanı']}"
            )

        with col3:
            st.metric(
                "En Düşük Boyut",
                lowest_dimension["Alt Boyut"],
                f"%{lowest_dimension['Yüzde Puanı']}"
            )

        st.divider()

        # Tablo
        st.markdown("### Sonuç Tablosu")
        display_df = result_df[[
            "Alt Boyut",
            "Ham Puan",
            "Maksimum Puan",
            "Yüzde Puanı",
            "Düzey"
        ]]

        st.dataframe(display_df, use_container_width=True)

        # Grafik
        st.markdown("### Grafiksel Gösterim")
        chart_df = result_df.set_index("Alt Boyut")["Yüzde Puanı"]
        st.bar_chart(chart_df)

        # Ayrıntılı yorumlar
        st.markdown("### Alt Boyut Yorumları")

        for _, row in result_df.iterrows():
            with st.expander(f"{row['Alt Boyut']} — {row['Düzey']} düzey"):
                st.write(f"**Puan:** {row['Ham Puan']} / {row['Maksimum Puan']}")
                st.write(f"**Yüzde Puanı:** %{row['Yüzde Puanı']}")
                st.write(f"**Yorum:** {row['Yorum']}")

        st.divider()

        # Rapor indirme
        st.markdown("### 📄 Rapor Oluştur")

        html_report = create_html_report(name.strip(), surname.strip(), result_df)
        text_report = create_text_report(name.strip(), surname.strip(), result_df)
        csv_data = result_df.to_csv(index=False).encode("utf-8-sig")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="HTML Raporu İndir",
                data=html_report,
                file_name=f"{name.strip()}_{surname.strip()}_mizac_karakter_raporu.html",
                mime="text/html"
            )

        with col2:
            st.download_button(
                label="Metin Raporu İndir",
                data=text_report,
                file_name=f"{name.strip()}_{surname.strip()}_mizac_karakter_raporu.txt",
                mime="text/plain"
            )

        with col3:
            st.download_button(
                label="Sonuçları CSV İndir",
                data=csv_data,
                file_name=f"{name.strip()}_{surname.strip()}_mizac_karakter_sonuclari.csv",
                mime="text/csv"
            )

        st.warning(
            "Bu uygulama klinik tanı koymak amacıyla kullanılmamalıdır. "
            "Sonuçlar yalnızca araştırma ve betimleyici değerlendirme amacıyla yorumlanmalıdır."
        )


# -------------------------------------------------
# Alt bilgi
# -------------------------------------------------
st.divider()

st.caption(
    "Cloninger’in mizaç ve karakter kuramına dayalı kısa değerlendirme formu. "
    "Bu uygulama araştırma amaçlı kullanım için hazırlanmıştır."
)
