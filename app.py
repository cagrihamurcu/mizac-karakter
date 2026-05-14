import streamlit as st
import pandas as pd
from datetime import datetime
import html


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
# -------------------------------------------------
SCALE_ITEMS = [
    {"dimension": "Yenilik Arayışı", "item": "Keşfetmekten heyecan duyarım."},
    {"dimension": "Yenilik Arayışı", "item": "Hızlı karar veririm."},
    {"dimension": "Yenilik Arayışı", "item": "Savurganım."},
    {"dimension": "Yenilik Arayışı", "item": "Düzensiz olduğumu düşünürüm."},

    {"dimension": "Zarardan Kaçınma", "item": "Endişeli ve karamsar olduğumu düşünürüm."},
    {"dimension": "Zarardan Kaçınma", "item": "Belirsizlikten korkarım."},
    {"dimension": "Zarardan Kaçınma", "item": "Yabancılardan çekinirim."},
    {"dimension": "Zarardan Kaçınma", "item": "Çabuk yorulurum."},

    {"dimension": "Ödül Bağımlılığı", "item": "Duygusal olduğumu düşünürüm."},
    {"dimension": "Ödül Bağımlılığı", "item": "Kolay bağlanırım."},
    {"dimension": "Ödül Bağımlılığı", "item": "Başka insanlara bağımlı bir yapım vardır."},

    {"dimension": "Sebat Etme", "item": "Mükemmeliyetçiyim."},
    {"dimension": "Sebat Etme", "item": "Amacıma ulaşmak için sınırları zorlarım."},
    {"dimension": "Sebat Etme", "item": "Kolay vazgeçmem."},
    {"dimension": "Sebat Etme", "item": "Sebat ederim."},

    {"dimension": "Kendi Kendini Yönetme", "item": "Sorumluluk alırım."},
    {"dimension": "Kendi Kendini Yönetme", "item": "Amaçlarımı kendim belirlerim."},
    {"dimension": "Kendi Kendini Yönetme", "item": "Becerikli olduğumu düşünürüm."},
    {"dimension": "Kendi Kendini Yönetme", "item": "Kendimi olduğum gibi kabullenirim."},
    {"dimension": "Kendi Kendini Yönetme", "item": "Değişikliklere kolay adapte olurum."},

    {"dimension": "İşbirliği Yapma", "item": "Başkalarını olduğu gibi kabullenirim."},
    {"dimension": "İşbirliği Yapma", "item": "Empati kurarım."},
    {"dimension": "İşbirliği Yapma", "item": "Yardım severim."},
    {"dimension": "İşbirliği Yapma", "item": "Acıma duygum vardır."},
    {"dimension": "İşbirliği Yapma", "item": "Temiz kalpli ve vicdanlıyım."},

    {"dimension": "Kendi Kendini Aşma", "item": "Yaptığım işe kendimi kaptırırım."},
    {"dimension": "Kendi Kendini Aşma", "item": "Çevremdeki insanları bir parçam olarak görürüm."},
    {
        "dimension": "Kendi Kendini Aşma",
        "item": "Hayatta manevi bir gücün yarattığı mükemmel bir düzen olduğuna inanırım."
    }
]


# -------------------------------------------------
# Sabit karışık soru sırası
# -------------------------------------------------
FIXED_SHUFFLED_ORDER = [
    5, 16, 0, 23, 11, 8, 20, 2, 26, 14, 4, 18, 9, 21,
    1, 12, 7, 24, 19, 10, 3, 15, 6, 22, 25, 13, 17, 27
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


# -------------------------------------------------
# Düzeye göre kısa yorumlar
# -------------------------------------------------
DIMENSION_DESCRIPTIONS = {
    "Yenilik Arayışı": {
        "Düşük": "Yenilik arayışı düşük düzeydedir. Katılımcı daha temkinli, düzenli ve alışılmış yöntemleri tercih eden bir yapı gösterebilir.",
        "Orta": "Yenilik arayışı orta düzeydedir. Katılımcı yeni deneyimlere zaman zaman açık olmakla birlikte, kararlarında denge ve ölçülülük gösterebilir.",
        "Yüksek": "Yenilik arayışı yüksek düzeydedir. Katılımcı keşfetmeye açık, yenilikten heyecan duyan, hızlı karar verebilen ve hareketli bir yapı gösterebilir."
    },
    "Zarardan Kaçınma": {
        "Düşük": "Zarardan kaçınma düşük düzeydedir. Katılımcı belirsizlikler karşısında daha rahat, cesur ve risk almaya daha açık olabilir.",
        "Orta": "Zarardan kaçınma orta düzeydedir. Katılımcı bazı durumlarda temkinli davranırken, bazı durumlarda daha rahat ve esnek olabilir.",
        "Yüksek": "Zarardan kaçınma yüksek düzeydedir. Katılımcı kaygılı, temkinli, belirsizlikten rahatsız olan, çekingen ve kolay yorulan bir yapı gösterebilir."
    },
    "Ödül Bağımlılığı": {
        "Düşük": "Ödül bağımlılığı düşük düzeydedir. Katılımcı ilişkilerinde daha bağımsız, duygusal etkilenmeye daha kapalı ve kendi kararlarını önceleyen bir yapı gösterebilir.",
        "Orta": "Ödül bağımlılığı orta düzeydedir. Katılımcı sosyal bağlara önem vermekle birlikte, ilişkilerinde görece dengeli ve bağımsız davranabilir.",
        "Yüksek": "Ödül bağımlılığı yüksek düzeydedir. Katılımcı duygusal, sosyal bağlara önem veren, kolay bağlanan ve başkalarından etkilenmeye açık bir yapı gösterebilir."
    },
    "Sebat Etme": {
        "Düşük": "Sebat etme düşük düzeydedir. Katılımcı zorlayıcı hedefler karşısında daha çabuk vazgeçebilir veya çabasını sürdürmekte zorlanabilir.",
        "Orta": "Sebat etme orta düzeydedir. Katılımcı hedefleri doğrultusunda çaba gösterebilir; ancak koşullara göre motivasyonu değişebilir.",
        "Yüksek": "Sebat etme yüksek düzeydedir. Katılımcı kararlı, hedefe bağlı, kolay vazgeçmeyen ve çabasını sürdüren bir yapı gösterebilir."
    },
    "Kendi Kendini Yönetme": {
        "Düşük": "Kendi kendini yönetme düşük düzeydedir. Katılımcı sorumluluk alma, amaç belirleme, kendini kabul etme veya uyum sağlama alanlarında zorlanabilir.",
        "Orta": "Kendi kendini yönetme orta düzeydedir. Katılımcı sorumluluk alma ve amaç belirleme konusunda genel olarak yeterli olmakla birlikte bazı alanlarda desteğe ihtiyaç duyabilir.",
        "Yüksek": "Kendi kendini yönetme yüksek düzeydedir. Katılımcı sorumluluk alan, amaçlarını belirleyebilen, kendini kabul eden, becerikli ve uyum sağlayabilen bir yapı gösterebilir."
    },
    "İşbirliği Yapma": {
        "Düşük": "İşbirliği yapma düşük düzeydedir. Katılımcı sosyal ilişkilerde daha mesafeli, bireysel hareket eden veya başkalarının ihtiyaçlarına karşı daha sınırlı duyarlılık gösteren bir yapı sergileyebilir.",
        "Orta": "İşbirliği yapma orta düzeydedir. Katılımcı sosyal ilişkilerde genel olarak uyumlu olmakla birlikte, bazı durumlarda bireysel sınırlarını daha fazla koruyabilir.",
        "Yüksek": "İşbirliği yapma yüksek düzeydedir. Katılımcı empatik, yardımsever, vicdanlı, başkalarını kabullenen ve sosyal uyuma önem veren bir yapı gösterebilir."
    },
    "Kendi Kendini Aşma": {
        "Düşük": "Kendi kendini aşma düşük düzeydedir. Katılımcı daha somut, gerçekçi ve bireysel sınırları belirgin bir anlam dünyasına sahip olabilir.",
        "Orta": "Kendi kendini aşma orta düzeydedir. Katılımcı zaman zaman manevi, bütüncül veya anlam odaklı düşünceler geliştirebilir.",
        "Yüksek": "Kendi kendini aşma yüksek düzeydedir. Katılımcı yaptığı işe kendini kaptırabilen, çevresiyle bütünlük hissedebilen ve manevi anlam arayışı güçlü bir yapı gösterebilir."
    }
}


# -------------------------------------------------
# Geniş değerlendirme içerikleri
# -------------------------------------------------
DIMENSION_DETAILS = {
    "Yenilik Arayışı": {
        "tanım": (
            "Yenilik Arayışı, yeni uyaranlara ve yeni deneyimlere yönelme eğilimidir. "
            "Kişinin keşfetmeye, araştırmaya ve denemeye açık olmasını ifade eder. "
            "Ödül ihtimali ortaya çıktığında hareketlenme ve heyecan artabilir."
        ),
        "davranışsal_görünüm": (
            "Karar alma sürecinde hızlı ve dürtüsel davranma eğilimi görülebilir. "
            "Yeni ve farklı olana karşı merak yüksektir. Engellenme durumunda sabırsızlık "
            "veya hızlı tepki ortaya çıkabilir."
        ),
        "güçlü_taraflar": ["Keşif", "Hız", "Değişim enerjisi"],
        "riskler": ["Dürtüsellik", "Dağınıklık", "Erken karar"],
        "liderlik_yorumu": (
            "Yenilik arayışı yüksek yöneticiler değişim başlatabilir. Ancak ekip hazır değilse "
            "bu enerji karmaşaya da dönüşebilir. Bu boyut ölçekte keşfetmekten heyecan duyma, "
            "hızlı karar verme, savurganlık ve düzensizlikle ilişkilendirilir."
        )
    },
    "Zarardan Kaçınma": {
        "tanım": (
            "Zarardan Kaçınma, riskli ve tehlikeli durumlara karşı temkinli olma eğilimidir. "
            "Kişi risk ve tehdit karşısında kaçınma veya geri çekilme davranışı gösterebilir. "
            "Belirsizlik bu kişiler için daha zorlayıcı olabilir."
        ),
        "davranışsal_görünüm": (
            "Yeni, bilinmeyen ve öngörülemeyen durumlara karşı çekingenlik görülebilir. "
            "Endişelilik ve karamsarlık daha belirgin olabilir. Riskten korunma ihtiyacı "
            "davranışı yönlendirebilir. Çabuk yorulma ve pasif kaçınma eğilimi görülebilir."
        ),
        "güçlü_taraflar": ["Risk fark etme", "Dikkat", "Temkin"],
        "riskler": ["Karar gecikmesi", "Aşırı güvence arama", "Değişime direnç"],
        "liderlik_yorumu": (
            "Bu boyut özellikle operasyon, güvenlik, kalite ve regülasyon gibi alanlarda değerlidir. "
            "Ancak aşırı olduğunda belirsizliğe toleransı azaltabilir. Ölçekte endişe, belirsizlik "
            "korkusu ve çekinme davranışı ile görünür."
        )
    },
    "Ödül Bağımlılığı": {
        "tanım": (
            "Ödül Bağımlılığı, duygusal ve sosyal bağ kurma eğilimini ifade eder. "
            "Kişi ilişkilerde yakınlık, kabul ve onay arayabilir. Başkalarının düşünce "
            "ve değerlendirmeleri daha etkili olabilir."
        ),
        "davranışsal_görünüm": (
            "Sosyal bağları sürdürme isteği yüksektir. Duygusal tepkiler ve ilişkisel hassasiyet "
            "daha belirgin olabilir. İnsanlarla bağ kurmaya ve bağlı kalmaya yatkınlık görülebilir."
        ),
        "güçlü_taraflar": ["İlişki kurma", "Aidiyet yaratma", "Duyarlılık"],
        "riskler": ["Onay arama", "Zor konuşmadan kaçınma", "Netlik kaybı"],
        "liderlik_yorumu": (
            "İlişki odaklı liderler ekipte bağlılık ve güven oluşturabilir. Ancak ilişkiyi koruma "
            "isteği bazen zor kararları ve net geri bildirimleri geciktirebilir."
        )
    },
    "Sebat Etme": {
        "tanım": (
            "Sebat Etme, zorlanma ve engellenme karşısında devam etme eğilimidir. "
            "Kişinin hedefe ulaşmak için ısrarcı ve kararlı davranmasını ifade eder. "
            "Yorgunluk ve engeller karşısında dayanıklılık gösterebilir."
        ),
        "davranışsal_görünüm": (
            "Sonuca ulaşma isteği güçlüdür. Kolay vazgeçmeme eğilimi öne çıkar. "
            "Bu boyutta kararlılık ve direnç belirgindir."
        ),
        "güçlü_taraflar": ["Kararlılık", "Dayanıklılık", "Hedefe odaklanma"],
        "riskler": ["Mükemmeliyetçilik", "Esneklik kaybı", "Tükenmişlik üretme"],
        "liderlik_yorumu": (
            "Sebat etme düzeyi yüksek olan yöneticiler işleri sonuçlandırma ve hedefe ulaşma konusunda güçlüdür. "
            "Ancak bu yüksek standart ve ısrar, ekip tarafından zaman zaman sürekli performans baskısı olarak algılanabilir. "
            "Ölçekte mükemmeliyetçilik, sınırları zorlama ve vazgeçmeme boyutları yer alır."
        )
    },
    "Kendi Kendini Yönetme": {
        "tanım": (
            "Kendi Kendini Yönetme, bireyin kendi seçim ve davranışlarının sorumluluğunu almasıyla ilgilidir. "
            "Amaçlarının farkında olma ve hedeflerini belirleme eğilimini içerir. "
            "Sorunlar karşısında etkin çözüm üretme becerisi öne çıkar."
        ),
        "davranışsal_görünüm": (
            "Sorumluluk duygusu ve görev bilinci yüksektir. Kişinin kendine güvenmesi ve kendini kabul etmesi "
            "bu boyutta önemlidir. Değişen koşullara uyum sağlama becerisi görülebilir."
        ),
        "güçlü_taraflar": ["Sorumluluk", "Hedef koyma", "Öz disiplin", "Uyum"],
        "riskler": ["Aşırı kontrol", "Yardım istememe", "Delege edememe", "Kendine aşırı yüklenme", "Esneklik kaybı"],
        "liderlik_yorumu": (
            "Liderliğin merkezi boyutlarından biridir. Kendi duygu, davranış ve önceliklerini yöneten kişi, "
            "ekibini de daha sağlıklı yönetebilir. Ölçekte sorumluluk alma, amaç belirleme, beceriklilik, "
            "kendini kabul ve değişime uyum yer alır."
        )
    },
    "İşbirliği Yapma": {
        "tanım": (
            "İşbirliği Yapma, başkalarıyla uyumlu ve yapıcı ilişki kurma eğilimidir. "
            "Kişinin başkalarını olduğu gibi kabul etmesi bu boyutta önemlidir. "
            "Hoşgörü ve empati kurma becerisi öne çıkar."
        ),
        "davranışsal_görünüm": (
            "Başkalarının duygularına karşı duyarlılık görülebilir. Yardımseverlik ve yararlı olma isteği belirgindir. "
            "Sevecen, vicdanlı ve sosyal kabule yatkın bir yapı görülebilir."
        ),
        "güçlü_taraflar": ["Empati", "Yardımseverlik", "Başkalarını kabul", "Güven yaratma"],
        "riskler": [
            "Sınır koymakta zorlanma",
            "Aşırı tolerans",
            "Zor konuşmaları erteleme",
            "Düşük performansa geç müdahale",
            "Herkesi memnun etmeye çalışma",
            "Çatışmadan kaçınma",
            "Netlik kaybı"
        ],
        "liderlik_yorumu": (
            "İşbirliği yapan lider ekipte güvenli iklim oluşturabilir. Ancak fazla tolerans performans yönetimini "
            "zorlaştırabilir. Ölçekte empati, yardımseverlik, vicdanlılık ve başkalarını kabul etme vurgulanır."
        )
    },
    "Kendi Kendini Aşma": {
        "tanım": (
            "Kendi Kendini Aşma, kişinin kendisini daha büyük bir anlam ve bütünün parçası olarak görmesiyle ilgilidir. "
            "İdealist ve yaratıcı bir yönü ifade eder. Bencillikten uzak, daha kapsayıcı bir bakış açısı içerebilir."
        ),
        "davranışsal_görünüm": (
            "İnanç, değerler ve manevi duygular bu boyutta etkili olabilir. Kişi yaptığı işe kendini derin biçimde verebilir. "
            "Çevresindeki insanları ve yaşamı daha bütünsel bir bakışla değerlendirebilir. Daha büyük bir düzen ve anlam "
            "duygusuna yönelim görülebilir."
        ),
        "güçlü_taraflar": ["Anlam duygusu", "Bütünsel bakış", "İlham", "Amaç odaklılık"],
        "riskler": ["Aşırı idealizm", "Soyut kalma", "Detayı kaçırma", "Gerçekçi olmayan iyimserlik", "Sınırların bulanıklaşması"],
        "liderlik_yorumu": (
            "Bu boyut liderin yalnızca ne yapıldığını değil, neden yapıldığını da görünür kılmasına yardımcı olabilir. "
            "Ancak sadece ilham yeterli değildir; operasyonel yön de gerekir. Ölçekte işe kendini kaptırma, çevresindekileri "
            "kendinin parçası olarak görme ve daha büyük bir düzene inanma yer alır."
        )
    }
}


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
            "Yorum": DIMENSION_DESCRIPTIONS[dimension][level]
        })

    return pd.DataFrame(results)


def create_profile_summary(df):
    highest_dimension = df.sort_values("Yüzde Puanı", ascending=False).iloc[0]
    lowest_dimension = df.sort_values("Yüzde Puanı", ascending=True).iloc[0]

    high_count = int((df["Düzey"] == "Yüksek").sum())
    medium_count = int((df["Düzey"] == "Orta").sum())
    low_count = int((df["Düzey"] == "Düşük").sum())

    high_dimensions = df[df["Düzey"] == "Yüksek"]["Alt Boyut"].tolist()
    medium_dimensions = df[df["Düzey"] == "Orta"]["Alt Boyut"].tolist()
    low_dimensions = df[df["Düzey"] == "Düşük"]["Alt Boyut"].tolist()

    return {
        "highest_dimension": highest_dimension,
        "lowest_dimension": lowest_dimension,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "high_dimensions": high_dimensions,
        "medium_dimensions": medium_dimensions,
        "low_dimensions": low_dimensions
    }


def format_dimension_list(items):
    if not items:
        return "Yok"
    return ", ".join(items)


def format_list_html(items):
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def format_list_text(items):
    return ", ".join(items) if items else "Yok"


def safe_file_name(text):
    cleaned = text.strip().replace(" ", "_")
    cleaned = "".join(char for char in cleaned if char.isalnum() or char in ["_", "-"])
    return cleaned if cleaned else "katilimci"


def create_html_report(participant_code, name, surname, df):
    full_name = f"{name} {surname}".strip()
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    profile = create_profile_summary(df)

    participant_name_html = html.escape(full_name) if full_name else "Belirtilmedi"

    rows = ""
    detail_sections = ""

    for _, row in df.iterrows():
        dimension = row["Alt Boyut"]
        detail = DIMENSION_DETAILS[dimension]

        rows += f"""
        <tr>
            <td>{html.escape(str(row['Alt Boyut']))}</td>
            <td>{row['Ham Puan']} / {row['Maksimum Puan']}</td>
            <td>%{row['Yüzde Puanı']}</td>
            <td><strong>{html.escape(str(row['Düzey']))}</strong></td>
            <td>{html.escape(str(row['Yorum']))}</td>
        </tr>
        """

        detail_sections += f"""
        <div class="dimension-card">
            <h3>{html.escape(dimension)} — {html.escape(str(row['Düzey']))} düzey</h3>
            <p><strong>Puan:</strong> {row['Ham Puan']} / {row['Maksimum Puan']} | 
            <strong>Yüzde Puanı:</strong> %{row['Yüzde Puanı']}</p>

            <h4>Tanım</h4>
            <p>{html.escape(detail['tanım'])}</p>

            <h4>Davranışsal Görünüm</h4>
            <p>{html.escape(detail['davranışsal_görünüm'])}</p>

            <h4>Katılımcı Yorumu</h4>
            <p>{html.escape(row['Yorum'])}</p>

            <h4>Güçlü Taraflar</h4>
            <ul>{format_list_html(detail['güçlü_taraflar'])}</ul>

            <h4>Dikkat Edilmesi Gereken Riskler</h4>
            <ul>{format_list_html(detail['riskler'])}</ul>

            <h4>Liderlik / Çalışma Yaşamı Açısından Değerlendirme</h4>
            <p>{html.escape(detail['liderlik_yorumu'])}</p>
        </div>
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
            h3 {{
                color: #243b53;
                margin-bottom: 5px;
            }}
            h4 {{
                color: #334e68;
                margin-bottom: 4px;
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
            .summary-box {{
                background-color: #eef8f4;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
            }}
            .dimension-card {{
                border: 1px solid #d9e2ec;
                border-radius: 10px;
                padding: 16px;
                margin-top: 18px;
                background-color: #ffffff;
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
            <p><strong>Katılımcı Kodu:</strong> {html.escape(participant_code)}</p>
            <p><strong>Katılımcı Adı Soyadı:</strong> {participant_name_html}</p>
            <p><strong>Rapor Tarihi:</strong> {date_str}</p>
        </div>

        <h2>Değerlendirme Yöntemi</h2>
        <p>
            Bu değerlendirmede her “Evet” yanıtı 1 puan, her “Hayır” yanıtı 0 puan olarak kabul edilmiştir.
            Ölçek maddeleri katılımcıya sabit karışık sırada ve alt boyut başlıkları gösterilmeden sunulmuştur.
            Her madde arka planda ait olduğu alt boyuta göre puanlanmıştır.
        </p>

        <p>
            Her alt boyuta ait maddeler toplanmış ve ilgili alt boyutun ham puanı elde edilmiştir.
            Alt boyutlarda madde sayıları farklı olduğu için puanlar yüzdelik değere dönüştürülmüştür.
            Yüzde puanları 0–33 arası düşük, 34–66 arası orta, 67–100 arası yüksek düzey olarak yorumlanmıştır.
        </p>

        <p>
            Bu değerlendirmede toplam puan hesaplanmamaktadır. Çünkü ölçek farklı mizaç ve karakter
            boyutlarını ayrı ayrı değerlendirmektedir. Bu nedenle sonuçlar toplam skor üzerinden değil,
            alt boyut profili üzerinden yorumlanmalıdır.
        </p>

        <h2>Profil Özeti</h2>
        <div class="summary-box">
            <p><strong>En belirgin boyut:</strong> {html.escape(str(profile["highest_dimension"]["Alt Boyut"]))}
            (%{profile["highest_dimension"]["Yüzde Puanı"]})</p>

            <p><strong>En düşük boyut:</strong> {html.escape(str(profile["lowest_dimension"]["Alt Boyut"]))}
            (%{profile["lowest_dimension"]["Yüzde Puanı"]})</p>

            <p><strong>Yüksek düzeydeki boyut sayısı:</strong> {profile["high_count"]}</p>
            <p><strong>Orta düzeydeki boyut sayısı:</strong> {profile["medium_count"]}</p>
            <p><strong>Düşük düzeydeki boyut sayısı:</strong> {profile["low_count"]}</p>

            <p><strong>Yüksek düzeyde çıkan boyutlar:</strong> {html.escape(format_dimension_list(profile["high_dimensions"]))}</p>
            <p><strong>Orta düzeyde çıkan boyutlar:</strong> {html.escape(format_dimension_list(profile["medium_dimensions"]))}</p>
            <p><strong>Düşük düzeyde çıkan boyutlar:</strong> {html.escape(format_dimension_list(profile["low_dimensions"]))}</p>
        </div>

        <h2>Sonuç Tablosu</h2>
        <table>
            <thead>
                <tr>
                    <th>Alt Boyut</th>
                    <th>Puan</th>
                    <th>Yüzde</th>
                    <th>Düzey</th>
                    <th>Kısa Yorum</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <h2>Ayrıntılı Alt Boyut Değerlendirmeleri</h2>
        {detail_sections}

        <div class="note">
            <strong>Not:</strong> Bu kısa form klinik tanı koymak amacıyla kullanılmamalıdır.
            Sonuçlar yalnızca araştırma kapsamında betimleyici kişilik özelliği değerlendirmesi olarak yorumlanmalıdır.
            Bilimsel çalışmalarda kullanılması durumunda ölçeğin geçerlik ve güvenirlik analizlerinin ayrıca yapılması önerilir.
        </div>
    </body>
    </html>
    """

    return report


def create_text_report(participant_code, name, surname, df):
    full_name = f"{name} {surname}".strip()
    if not full_name:
        full_name = "Belirtilmedi"

    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    profile = create_profile_summary(df)

    report = f"""
MİZAÇ VE KARAKTER ÖZELLİKLERİ DEĞERLENDİRME RAPORU

Katılımcı Kodu: {participant_code}
Katılımcı Adı Soyadı: {full_name}
Rapor Tarihi: {date_str}

DEĞERLENDİRME YÖNTEMİ
Her “Evet” yanıtı 1 puan, her “Hayır” yanıtı 0 puan olarak kodlanmıştır.
Ölçek maddeleri katılımcıya sabit karışık sırada ve alt boyut başlıkları gösterilmeden sunulmuştur.
Her madde arka planda ait olduğu alt boyuta göre puanlanmıştır.
Her alt boyuta ait maddeler toplanarak ham puan elde edilmiştir.
Madde sayıları farklı olduğu için ham puanlar yüzdelik puana dönüştürülmüştür.
0–33 düşük, 34–66 orta, 67–100 yüksek düzey olarak yorumlanmıştır.

Bu değerlendirmede toplam puan hesaplanmamaktadır. Çünkü ölçek farklı mizaç ve karakter
boyutlarını ayrı ayrı değerlendirmektedir. Bu nedenle sonuçlar toplam skor üzerinden değil,
alt boyut profili üzerinden yorumlanmalıdır.

PROFİL ÖZETİ
En belirgin boyut: {profile["highest_dimension"]["Alt Boyut"]} (%{profile["highest_dimension"]["Yüzde Puanı"]})
En düşük boyut: {profile["lowest_dimension"]["Alt Boyut"]} (%{profile["lowest_dimension"]["Yüzde Puanı"]})

Yüksek düzeydeki boyut sayısı: {profile["high_count"]}
Orta düzeydeki boyut sayısı: {profile["medium_count"]}
Düşük düzeydeki boyut sayısı: {profile["low_count"]}

Yüksek düzeyde çıkan boyutlar: {format_dimension_list(profile["high_dimensions"])}
Orta düzeyde çıkan boyutlar: {format_dimension_list(profile["medium_dimensions"])}
Düşük düzeyde çıkan boyutlar: {format_dimension_list(profile["low_dimensions"])}

SONUÇLAR
"""

    for _, row in df.iterrows():
        dimension = row["Alt Boyut"]
        detail = DIMENSION_DETAILS[dimension]

        report += f"""
------------------------------------------------------------
{dimension} — {row['Düzey']} düzey
------------------------------------------------------------

Puan: {row['Ham Puan']} / {row['Maksimum Puan']}
Yüzde Puanı: %{row['Yüzde Puanı']}

Tanım:
{detail['tanım']}

Davranışsal Görünüm:
{detail['davranışsal_görünüm']}

Katılımcı Yorumu:
{row['Yorum']}

Güçlü Taraflar:
{format_list_text(detail['güçlü_taraflar'])}

Dikkat Edilmesi Gereken Riskler:
{format_list_text(detail['riskler'])}

Liderlik / Çalışma Yaşamı Açısından Değerlendirme:
{detail['liderlik_yorumu']}
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
Maddeler sabit karışık sırada sunulmaktadır. Değerlendirme sonunda kişisel bir rapor oluşturulacaktır.
""")

with st.expander("ℹ️ Puanlama hakkında bilgi"):
    st.markdown("""
    - **Evet = 1 puan**
    - **Hayır = 0 puan**
    - Maddeler katılımcıya sabit karışık sırada gösterilir.
    - Alt boyut başlıkları form ekranında gösterilmez.
    - Her madde arka planda ait olduğu alt boyuta göre puanlanır.
    - Sonuçlar yüzde puana dönüştürülür.
    - **0–33:** Düşük  
    - **34–66:** Orta  
    - **67–100:** Yüksek
    - Toplam puan hesaplanmaz; sonuçlar alt boyut profili üzerinden değerlendirilir.
    """)

st.divider()


# -------------------------------------------------
# Onam bölümü
# -------------------------------------------------
st.subheader("I. Bilgilendirme ve Onam")

st.info(
    "Bu form araştırma ve betimleyici değerlendirme amacıyla hazırlanmıştır. "
    "Elde edilen sonuçlar klinik tanı koyma amacı taşımaz. "
    "Lütfen maddeleri içtenlikle yanıtlayınız. Doğru ya da yanlış cevap yoktur."
)

consent = st.checkbox(
    "Bilgilendirme metnini okudum, anladım ve bu değerlendirmeye katılmayı kabul ediyorum."
)

if not consent:
    st.warning("Forma devam edebilmek için bilgilendirme ve onam kutusunu işaretlemeniz gerekmektedir.")
    st.stop()


st.divider()


# -------------------------------------------------
# Katılımcı bilgileri
# -------------------------------------------------
st.subheader("II. Katılımcı Bilgileri")

participant_code = st.text_input(
    "Katılımcı Kodu *",
    placeholder="Örn. K001, P023, ANK-045"
)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Adınız",
        placeholder="Örn. Ayşe",
        help="İsteğe bağlıdır. Anonim kullanım için boş bırakılabilir."
    )

with col2:
    surname = st.text_input(
        "Soyadınız",
        placeholder="Örn. Yılmaz",
        help="İsteğe bağlıdır. Anonim kullanım için boş bırakılabilir."
    )


st.divider()


# -------------------------------------------------
# Form
# -------------------------------------------------
st.subheader("III. Değerlendirme Maddeleri")

answers = {}

with st.form("personality_form"):
    for display_number, original_index in enumerate(FIXED_SHUFFLED_ORDER, start=1):
        scale_item = SCALE_ITEMS[original_index]

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
    if not participant_code.strip():
        st.error("Lütfen katılımcı kodunu giriniz.")

    elif any(value is None for value in answers.values()):
        st.error("Lütfen tüm maddeleri işaretleyiniz. Boş madde bırakılmamalıdır.")

    else:
        numeric_answers = {
            key: value for key, value in answers.items()
            if value is not None
        }

        result_df = create_results(numeric_answers)
        profile = create_profile_summary(result_df)

        st.success("Değerlendirme başarıyla tamamlandı.")

        full_name = f"{name.strip()} {surname.strip()}".strip()
        display_identity = participant_code.strip()
        if full_name:
            display_identity += f" - {full_name}"

        st.subheader(f"📌 {display_identity} için Değerlendirme Sonuçları")

        st.info(
            "Bu değerlendirmede toplam puan hesaplanmamaktadır. "
            "Çünkü ölçek farklı mizaç ve karakter boyutlarını ayrı ayrı değerlendirmektedir. "
            "Bu nedenle sonuçlar toplam skor üzerinden değil, alt boyut profili üzerinden yorumlanmalıdır."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "En Belirgin Boyut",
                profile["highest_dimension"]["Alt Boyut"],
                f"%{profile['highest_dimension']['Yüzde Puanı']}"
            )

        with col2:
            st.metric(
                "En Düşük Boyut",
                profile["lowest_dimension"]["Alt Boyut"],
                f"%{profile['lowest_dimension']['Yüzde Puanı']}"
            )

        with col3:
            st.metric(
                "Profil Dağılımı",
                f"{profile['high_count']} yüksek",
                f"{profile['medium_count']} orta, {profile['low_count']} düşük"
            )

        st.markdown("### Profil Özeti")

        st.write(f"**Yüksek düzeyde çıkan boyutlar:** {format_dimension_list(profile['high_dimensions'])}")
        st.write(f"**Orta düzeyde çıkan boyutlar:** {format_dimension_list(profile['medium_dimensions'])}")
        st.write(f"**Düşük düzeyde çıkan boyutlar:** {format_dimension_list(profile['low_dimensions'])}")

        st.divider()

        st.markdown("### Sonuç Tablosu")

        display_df = result_df[[
            "Alt Boyut",
            "Ham Puan",
            "Maksimum Puan",
            "Yüzde Puanı",
            "Düzey"
        ]]

        st.dataframe(display_df, use_container_width=True)

        st.markdown("### Grafiksel Gösterim")
        chart_df = result_df.set_index("Alt Boyut")["Yüzde Puanı"]
        st.bar_chart(chart_df)

        st.markdown("### Ayrıntılı Alt Boyut Değerlendirmeleri")

        for _, row in result_df.iterrows():
            dimension = row["Alt Boyut"]
            detail = DIMENSION_DETAILS[dimension]

            with st.expander(f"{dimension} — {row['Düzey']} düzey"):
                st.write(f"**Puan:** {row['Ham Puan']} / {row['Maksimum Puan']}")
                st.write(f"**Yüzde Puanı:** %{row['Yüzde Puanı']}")

                st.markdown("#### Tanım")
                st.write(detail["tanım"])

                st.markdown("#### Davranışsal Görünüm")
                st.write(detail["davranışsal_görünüm"])

                st.markdown("#### Katılımcı Yorumu")
                st.write(row["Yorum"])

                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("#### Güçlü Taraflar")
                    for item in detail["güçlü_taraflar"]:
                        st.write(f"- {item}")

                with col_b:
                    st.markdown("#### Dikkat Edilmesi Gereken Riskler")
                    for item in detail["riskler"]:
                        st.write(f"- {item}")

                st.markdown("#### Liderlik / Çalışma Yaşamı Açısından Değerlendirme")
                st.write(detail["liderlik_yorumu"])

        st.divider()

        st.markdown("### 📄 Rapor Oluştur")

        participant_code_clean = participant_code.strip()
        file_base = safe_file_name(participant_code_clean)

        html_report = create_html_report(
            participant_code_clean,
            name.strip(),
            surname.strip(),
            result_df
        )

        text_report = create_text_report(
            participant_code_clean,
            name.strip(),
            surname.strip(),
            result_df
        )

        csv_data = result_df.to_csv(index=False).encode("utf-8-sig")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="HTML Raporu İndir",
                data=html_report,
                file_name=f"{file_base}_mizac_karakter_raporu.html",
                mime="text/html"
            )

        with col2:
            st.download_button(
                label="Metin Raporu İndir",
                data=text_report,
                file_name=f"{file_base}_mizac_karakter_raporu.txt",
                mime="text/plain"
            )

        with col3:
            st.download_button(
                label="Sonuçları CSV İndir",
                data=csv_data,
                file_name=f"{file_base}_mizac_karakter_sonuclari.csv",
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
