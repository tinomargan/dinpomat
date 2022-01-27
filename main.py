import streamlit as st
import camelot
import re
import io
import datetime
import create_event


now = datetime.datetime.now()

st.title("Dobrodošli na DINPOMAT!")
st.markdown("""**Dinpomat** je _web servis_ koji studentima Odjela
za informatiku omogućuje automatizirani unos najvažnijih aktivnosti
iz DINP-a u Google Calendar. Sve što treba je upisati ime
kolegija i zalijepiti poveznicu na DINP ili ga _uploadati_ u .pdf
formatu preko jednostavnog sučelja. Nakon toga ponudit će Vam se
gumb za unos aktivnosti u Google Calendar.""")

naziv_predmeta = st.text_input("Upišite naziv kolegija:")

# LINK INPUT

user_input = st.text_input("Zalijepite link od DINP-a i kliknite na gumb:")
datum = []
vrijeme = []
ucionica = []
naziv = []

if st.button("Kliknite!"):

    if len(naziv_predmeta) == 0:
        st.write("Morate unijeti naziv kolegija!")
    elif len(user_input) == 0:
        st.write("Morate zalijepiti link na DINP!")
    else:
        file = user_input

        tables = camelot.read_pdf(file, pages="5-end")

        aktivnosti = []
        for d in range(0, tables.n):
            l = tables[d].df
            for i in range(0, len(l)):
                l[4][i] = re.sub('\\n', '', l[4][i])
                l[2][i] = re.sub('\\n', '', l[2][i])

                akt_re2 = re.compile(
                    r'(Kolokvij|kolokvij|KOLOKVIJ|{Test|TEST|test}|Kviz|KVIZ|kviz|labo|LABO|Labo|Provjer|PROVJER|provjer)')

            for i in range(0, len(l)):
                if akt_re2.search(l[4][i]):
                    aktivnosti.append(l[1][i])
                    aktivnosti.append(l[2][i])
                    aktivnosti.append(l[3][i])
                    aktivnosti.append(l[4][i])

        for j in range(0, len(aktivnosti) - 1, 4):
            datum.append(aktivnosti[j])
        for j in range(0, len(aktivnosti) - 1, 4):
            vrijeme.append(aktivnosti[j + 1])
        for j in range(0, len(aktivnosti) - 1, 4):
            ucionica.append(aktivnosti[j + 2])
        for j in range(0, len(aktivnosti) - 1, 4):
            naziv.append(aktivnosti[j + 3])

        mjeseci = []
        datum_split = []

        for i in range(len(datum)):
            datum_split = datum[i].split(".")
            mjeseci.append(int(datum_split[1]))

        if len(datum[0]) <= 6:
            for i in range(len(datum)):
                if mjeseci[i] > 8 and mjeseci[i] < 13 and now.month > 8 and now.month < 13:
                    godina = str(now.year)
                    datum[i] = datum[i] + godina + "."
                elif mjeseci[i] > 8 and mjeseci[i] < 13 and not (now.month > 8 and now.month < 13):
                    godina = str(now.year - 1)
                    datum[i] = datum[i] + godina + "."
                elif not (mjeseci[i] > 8 and mjeseci[i] < 13) and now.month > 8 and now.month < 13:
                    godina = str(now.year + 1)
                    datum[i] = datum[i] + godina + "."
                else:
                    godina = str(now.year)
                    datum[i] = datum[i] + godina + "."

        for i in range(len(datum)):
            st.write(naziv_predmeta, i + 1, " ", datum[i], vrijeme[i], ucionica[i], naziv[i])

        st.success("Aktivnosti iz DINP-a uspješno su parsirane!")

        for i in range(len(datum)):
            create_event.create_event(str(datum[i]),str(vrijeme[i]),str(naziv_predmeta),str(ucionica[i]),str(naziv[i]))

        st.success("Parsirane aktivnosti uspješno su unesene u Vaš Google kalendar!")

# FILE UPLOAD


file = st.file_uploader("Ili prenesite DINP u .pdf formatu:", type=['pdf'])

if file is not None:
    if len(naziv_predmeta) == 0:
        st.write("Morate unijeti naziv kolegija!")
    else:

        g = io.BytesIO(file.read())
        temporary_location = "temp.pdf"

        with open(temporary_location, 'wb') as out:
            out.write(g.read())

        tables = camelot.read_pdf(temporary_location, pages="5-end")

        aktivnosti = []
        for d in range(0, tables.n):
            l = tables[d].df
            for i in range(0, len(l)):
                l[4][i] = re.sub('\\n', '', l[4][i])
                l[2][i] = re.sub('\\n', '', l[2][i])

                akt_re2 = re.compile(
                    r'(Kolokvij|kolokvij|KOLOKVIJ|{Test|TEST|test}|Kviz|KVIZ|kviz|labo|LABO|Labo|Provjer|PROVJER|provjer)')

            for i in range(0, len(l)):
                if akt_re2.search(l[4][i]):
                    aktivnosti.append(l[1][i])
                    aktivnosti.append(l[2][i])
                    aktivnosti.append(l[3][i])
                    aktivnosti.append(l[4][i])

        datum = []
        vrijeme = []
        ucionica = []
        naziv = []

        for j in range(0, len(aktivnosti) - 1, 4):
            datum.append(aktivnosti[j])
        for j in range(0, len(aktivnosti) - 1, 4):
            vrijeme.append(aktivnosti[j + 1])
        for j in range(0, len(aktivnosti) - 1, 4):
            ucionica.append(aktivnosti[j + 2])
        for j in range(0, len(aktivnosti) - 1, 4):
            naziv.append(aktivnosti[j + 3])

        mjeseci = []
        datum_split = []

        for i in range(len(datum)):
            datum_split = datum[i].split(".")
            mjeseci.append(int(datum_split[1]))

        if len(datum[0]) <= 6:
            for i in range(len(datum)):
                if mjeseci[i] > 8 and mjeseci[i] < 13 and now.month > 8 and now.month < 13:
                    godina = str(now.year)
                    datum[i] = datum[i] + godina + "."
                elif mjeseci[i] > 8 and mjeseci[i] < 13 and not (now.month > 8 and now.month < 13):
                    godina = str(now.year - 1)
                    datum[i] = datum[i] + godina + "."
                elif not (mjeseci[i] > 8 and mjeseci[i] < 13) and now.month > 8 and now.month < 13:
                    godina = str(now.year + 1)
                    datum[i] = datum[i] + godina + "."
                else:
                    godina = str(now.year)
                    datum[i] = datum[i] + godina + "."

        for i in range(len(datum)):
            st.write(naziv_predmeta, i + 1, " ", datum[i], vrijeme[i], ucionica[i], naziv[i])

        st.success("Aktivnosti iz DINP-a uspješno su parsirane!")

        for i in range(len(datum)):
            create_event.create_event(str(datum[i]), str(vrijeme[i]), str(naziv_predmeta), str(ucionica[i]),
                                      str(naziv[i]))

        st.success("Parsirane aktivnosti uspješno su unesene u Vaš Google kalendar!")
        out.close()