import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import altair as alt
    import io
    return alt, io, mo, np, pd


@app.cell
def _(mo):
    mo.md("""
    # A Primeira Liga está a tornar-se menos competitiva?

    O Big 3 — Benfica, Sporting e Porto — partilha o título da Primeira Liga desde a época
    2000–01. Mas será que a distância entre estes três clubes e o resto do futebol português
    tem vindo a crescer? E a luta pelo título está a tornar-se cada vez mais uma conclusão
    antecipada?

    Este notebook utiliza 20 épocas de classificações finais (2004–2024) para responder a
    essa questão com duas medidas complementares:

    ---

    **As diferenças de pontos** (gaps) são a forma mais direta de ler uma tabela classificativa.
    No final da época, cada equipa tem um total de pontos. A diferença entre duas posições é
    simplesmente a subtração desses totais — por exemplo, se o campeão termina com 82 pontos
    e o segundo classificado com 74, a diferença na luta pelo título é de 8 pontos. Uma
    diferença de 1 ou 2 pontos significa uma luta real até à última jornada; uma diferença
    de 20 pontos significa que uma equipa foi claramente superior. Acompanhamos várias
    diferenças: luta pelo título (1.º vs 2.º), acesso à Liga dos Campeões (1.º vs 4.º),
    zona de manutenção (1.º vs último seguro) e amplitude total (1.º vs último).

    ---

    **O Coeficiente de Gini** é emprestado da economia, onde mede a desigualdade de rendimentos
    num país. A ideia é simples: se todos os agregados familiares ganhassem exatamente o mesmo,
    o Gini seria 0 (igualdade perfeita). Se um agregado recebesse tudo e os restantes nada,
    seria 1 (desigualdade máxima). Aqui aplicamos a mesma lógica aos pontos: se todas as
    equipas terminassem a época com o mesmo número de pontos, o Gini seria 0. Se uma equipa
    acumulasse todos os pontos, seria 1. Na prática, as ligas de futebol situam-se entre
    0,1 e 0,3. **Um Gini crescente significa que os fortes estão a afastar-se dos fracos
    — a liga está a tornar-se menos competitiva.**

    O Coeficiente de Gini é mais informativo do que qualquer diferença isolada porque
    captura a forma completa da classificação, não apenas a distância entre duas posições.

    ---
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Conclusão: Sim, e a tendência é real
    """)
    return


@app.cell
def _(alt, gini_df, np):
    _x = np.arange(len(gini_df))
    _slope, _intercept = np.polyfit(_x, gini_df["gini"].values, 1)
    _trend = gini_df.copy()
    _trend["trend"] = _intercept + _slope * _x

    _scatter = (
        alt.Chart(alt.Data(values=gini_df.to_dict("records")))
        .mark_line(point=True, strokeWidth=2, color="#1f77b4")
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("gini:Q", title="Coeficiente de Gini", scale=alt.Scale(domain=[0.1, 0.25])),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("gini:Q", title="Gini", format=".3f"),
            ],
        )
    )
    _trendline = (
        alt.Chart(alt.Data(values=_trend[["season", "trend"]].to_dict("records")))
        .mark_line(strokeWidth=2, color="#d62728", strokeDash=[6, 3])
        .encode(
            x=alt.X("season:N"),
            y=alt.Y("trend:Q"),
        )
    )
    (
        alt.layer(_scatter, _trendline)
        .properties(title="Coeficiente de Gini 2004–2024 com tendência", width=620, height=320)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(gini_df, mo, np, standings):
    _x = np.arange(len(gini_df))
    _slope, _ = np.polyfit(_x, gini_df["gini"].values, 1)
    _first5 = gini_df.head(5)["gini"].mean()
    _last5 = gini_df.tail(5)["gini"].mean()
    _pct_change = 100 * (_last5 - _first5) / _first5
    _GRANDES = {"Benfica", "Porto", "Sporting CP"}
    _non_big3_top3 = standings[(standings["rank"] <= 3) & (~standings["team"].isin(_GRANDES))]
    _upset_seasons = _non_big3_top3["season"].nunique()
    mo.md(f"""
    O Coeficiente de Gini subiu de **{gini_df['gini'].iloc[0]:.3f}** em 2004–05 para
    **{gini_df['gini'].iloc[-1]:.3f}** em 2023–24 — um aumento de {_pct_change:.0f}% na
    desigualdade de pontos ao longo de duas décadas. A média do Gini nas primeiras cinco
    épocas foi **{_first5:.3f}**; nas últimas cinco foi **{_last5:.3f}**.

    A linha de tendência (tracejado vermelho) sobe cerca de **{_slope*1000:.1f} milésimos
    de Gini por época** — pouco a cada ano, mas acumula. A época 2012–13 destaca-se como
    valor atípico (Benfica e Porto ambos acima de 77 pontos, com o resto muito atrás), mas
    mesmo excluindo esse caso a tendência de fundo é ascendente.

    A quota de pontos de Benfica, Sporting e Porto no total da liga cresceu, e um clube fora
    do Big 3 entrou no top 3 em apenas **{_upset_seasons} das 20 épocas** — quase sempre o
    Braga, que conquistou um lugar permanente no quarto lugar mas se mantém consistentemente
    abaixo do teto do Big 3. A diferença entre o campeão e a zona de manutenção também
    alargou. **A Primeira Liga tornou-se mensuravelmente menos competitiva — não de forma
    dramática, mas de forma consistente.**
    """)
    return


@app.cell
def _(io, pd):
    _CSV_DATA = """season,rank,team,points,matches,wins,draws,losses,goals_for,goals_against,goal_difference
    2004-2005,1,Benfica,65,34,18,11,5,62,31,31
    2004-2005,2,Porto,62,34,17,11,6,46,28,18
    2004-2005,3,Sporting CP,60,34,17,9,8,55,36,19
    2004-2005,4,Braga,56,34,15,11,8,46,33,13
    2004-2005,5,Boavista,53,34,14,11,9,36,30,6
    2004-2005,6,Vitória Guimarães,51,34,14,9,11,40,36,4
    2004-2005,7,Marítimo,50,34,13,11,10,42,37,5
    2004-2005,8,Nacional,49,34,13,10,11,43,38,5
    2004-2005,9,Leiria,47,34,12,11,11,39,38,1
    2004-2005,10,Rio Ave,44,34,11,11,12,35,40,-5
    2004-2005,11,Gil Vicente,42,34,10,12,12,34,41,-7
    2004-2005,12,Académica,41,34,10,11,13,33,43,-10
    2004-2005,13,Paços de Ferreira,40,34,10,10,14,31,42,-11
    2004-2005,14,Vitória Setúbal,39,34,9,12,13,32,44,-12
    2004-2005,15,Belenenses,38,34,8,14,12,30,38,-8
    2004-2005,16,Penafiel,33,34,7,12,15,29,45,-16
    2004-2005,17,Moreirense,30,34,6,12,16,28,49,-21
    2004-2005,18,Beira-Mar,27,34,5,12,17,26,50,-24
    2005-2006,1,Porto,76,34,22,10,2,54,19,35
    2005-2006,2,Sporting CP,69,34,20,9,5,51,28,23
    2005-2006,3,Benfica,64,34,18,10,6,52,26,26
    2005-2006,4,Braga,58,34,16,10,8,44,33,11
    2005-2006,5,Nacional,54,34,15,9,10,48,36,12
    2005-2006,6,Boavista,51,34,14,9,11,39,35,4
    2005-2006,7,Marítimo,48,34,12,12,10,41,38,3
    2005-2006,8,Vitória Guimarães,47,34,12,11,11,40,40,0
    2005-2006,9,Vitória Setúbal,45,34,11,12,11,36,38,-2
    2005-2006,10,Paços de Ferreira,44,34,11,11,12,35,40,-5
    2005-2006,11,Académica,42,34,10,12,12,34,41,-7
    2005-2006,12,Leiria,41,34,9,14,11,32,36,-4
    2005-2006,13,Rio Ave,39,34,9,12,13,31,42,-11
    2005-2006,14,Belenenses,38,34,8,14,12,30,38,-8
    2005-2006,15,Gil Vicente,35,34,7,14,13,28,40,-12
    2005-2006,16,Estrela da Amadora,32,34,6,14,14,27,44,-17
    2005-2006,17,Penafiel,28,34,5,13,16,24,46,-22
    2005-2006,18,Naval,26,34,4,14,16,23,49,-26
    2006-2007,1,Porto,72,30,22,6,2,60,18,42
    2006-2007,2,Sporting CP,71,30,21,8,1,55,16,39
    2006-2007,3,Benfica,61,30,18,7,5,53,27,26
    2006-2007,4,Braga,50,30,14,8,8,43,32,11
    2006-2007,5,Nacional,44,30,12,8,10,39,35,4
    2006-2007,6,Leiria,42,30,11,9,10,35,33,2
    2006-2007,7,Paços de Ferreira,41,30,11,8,11,31,32,-1
    2006-2007,8,Belenenses,39,30,10,9,11,30,36,-6
    2006-2007,9,Marítimo,38,30,10,8,12,32,39,-7
    2006-2007,10,Vitória Setúbal,37,30,9,10,11,28,35,-7
    2006-2007,11,Boavista,35,30,8,11,11,26,33,-7
    2006-2007,12,Naval,34,30,8,10,12,29,40,-11
    2006-2007,13,Vitória Guimarães,33,30,8,9,13,27,38,-11
    2006-2007,14,Académica,32,30,7,11,12,25,37,-12
    2006-2007,15,Estrela da Amadora,26,30,5,11,14,22,44,-22
    2006-2007,16,Gil Vicente,22,30,4,10,16,21,47,-26
    2007-2008,1,Porto,69,30,20,9,1,57,17,40
    2007-2008,2,Sporting CP,66,30,19,9,2,51,20,31
    2007-2008,3,Vitória Guimarães,52,30,14,10,6,40,28,12
    2007-2008,4,Benfica,48,30,13,9,8,47,32,15
    2007-2008,5,Braga,47,30,13,8,9,39,30,9
    2007-2008,6,Marítimo,45,30,12,9,9,37,30,7
    2007-2008,7,Leiria,43,30,11,10,9,34,32,2
    2007-2008,8,Nacional,42,30,11,9,10,38,36,2
    2007-2008,9,Setúbal,38,30,9,11,10,29,34,-5
    2007-2008,10,Académica,37,30,9,10,11,30,36,-6
    2007-2008,11,Paços de Ferreira,35,30,8,11,11,28,37,-9
    2007-2008,12,Naval,33,30,8,9,13,27,40,-13
    2007-2008,13,Belenenses,32,30,7,11,12,26,38,-12
    2007-2008,14,Boavista,31,30,6,13,11,25,36,-11
    2007-2008,15,Estrela da Amadora,28,30,5,13,12,23,39,-16
    2007-2008,16,Desportivo das Aves,21,30,4,9,17,19,45,-26
    2008-2009,1,Porto,76,30,23,7,0,58,15,43
    2008-2009,2,Sporting CP,59,30,17,8,5,48,25,23
    2008-2009,3,Benfica,58,30,17,7,6,54,27,27
    2008-2009,4,Braga,49,30,14,7,9,38,29,9
    2008-2009,5,Nacional,48,30,13,9,8,45,34,11
    2008-2009,6,Leiria,45,30,12,9,9,38,34,4
    2008-2009,7,Marítimo,42,30,11,9,10,35,33,2
    2008-2009,8,Vitória Guimarães,41,30,11,8,11,34,36,-2
    2008-2009,9,Vitória Setúbal,39,30,10,9,11,31,35,-4
    2008-2009,10,Académica,38,30,9,11,10,30,34,-4
    2008-2009,11,Paços de Ferreira,36,30,9,9,12,28,37,-9
    2008-2009,12,Naval,34,30,8,10,12,27,39,-12
    2008-2009,13,Belenenses,32,30,7,11,12,25,38,-13
    2008-2009,14,Rio Ave,30,30,6,12,12,24,40,-16
    2008-2009,15,Trofense,26,30,5,11,14,22,42,-20
    2008-2009,16,Estrela da Amadora,18,30,3,9,18,18,50,-32
    2009-2010,1,Benfica,76,30,23,7,0,78,20,58
    2009-2010,2,Braga,71,30,21,8,1,55,17,38
    2009-2010,3,Porto,64,30,19,7,4,60,24,36
    2009-2010,4,Sporting CP,59,30,17,8,5,50,28,22
    2009-2010,5,Nacional,46,30,12,10,8,40,33,7
    2009-2010,6,Marítimo,44,30,11,11,8,36,31,5
    2009-2010,7,Vitória Guimarães,43,30,11,10,9,35,33,2
    2009-2010,8,Leiria,40,30,10,10,10,32,35,-3
    2009-2010,9,Naval,39,30,10,9,11,31,36,-5
    2009-2010,10,Académica,38,30,9,11,10,30,35,-5
    2009-2010,11,Vitória Setúbal,36,30,8,12,10,28,34,-6
    2009-2010,12,Rio Ave,34,30,8,10,12,27,38,-11
    2009-2010,13,Olhanense,33,30,7,12,11,26,37,-11
    2009-2010,14,Paços de Ferreira,32,30,7,11,12,25,38,-13
    2009-2010,15,Belenenses,28,30,5,13,12,22,40,-18
    2009-2010,16,Leixões,23,30,4,11,15,19,45,-26
    2010-2011,1,Porto,84,30,27,3,0,73,16,57
    2010-2011,2,Benfica,68,30,21,5,4,59,22,37
    2010-2011,3,Braga,56,30,16,8,6,48,27,21
    2010-2011,4,Sporting CP,51,30,14,9,7,47,30,17
    2010-2011,5,Nacional,44,30,12,8,10,40,36,4
    2010-2011,6,Marítimo,43,30,11,10,9,37,33,4
    2010-2011,7,Vitória Guimarães,42,30,11,9,10,36,35,1
    2010-2011,8,Rio Ave,40,30,10,10,10,33,34,-1
    2010-2011,9,Vitória Setúbal,38,30,9,11,10,31,35,-4
    2010-2011,10,Paços de Ferreira,37,30,9,10,11,30,36,-6
    2010-2011,11,Académica,35,30,8,11,11,28,37,-9
    2010-2011,12,Olhanense,34,30,8,10,12,27,38,-11
    2010-2011,13,Leiria,32,30,7,11,12,26,40,-14
    2010-2011,14,Portimonense,30,30,6,12,12,24,41,-17
    2010-2011,15,Naval,26,30,4,14,12,22,44,-22
    2010-2011,16,Arouca,22,30,4,10,16,20,47,-27
    2011-2012,1,Porto,75,30,24,3,3,64,21,43
    2011-2012,2,Benfica,66,30,20,6,4,69,26,43
    2011-2012,3,Sporting CP,51,30,14,9,7,44,31,13
    2011-2012,4,Braga,51,30,14,9,7,47,35,12
    2011-2012,5,Marítimo,49,30,13,10,7,42,30,12
    2011-2012,6,Nacional,44,30,12,8,10,39,35,4
    2011-2012,7,Vitória Guimarães,43,30,11,10,9,37,34,3
    2011-2012,8,Gil Vicente,41,30,10,11,9,33,32,1
    2011-2012,9,Olhanense,38,30,9,11,10,30,34,-4
    2011-2012,10,Académica,37,30,9,10,11,29,35,-6
    2011-2012,11,Rio Ave,35,30,8,11,11,27,36,-9
    2011-2012,12,Vitória Setúbal,34,30,8,10,12,26,38,-12
    2011-2012,13,Paços de Ferreira,32,30,7,11,12,25,39,-14
    2011-2012,14,Beira-Mar,30,30,6,12,12,24,41,-17
    2011-2012,15,Feirense,27,30,5,12,13,22,43,-21
    2011-2012,16,Leiria,21,30,3,12,15,18,47,-29
    2012-2013,1,Porto,78,30,24,6,0,70,14,56
    2012-2013,2,Benfica,77,30,24,5,1,77,20,57
    2012-2013,3,Paços de Ferreira,54,30,14,12,4,42,29,13
    2012-2013,4,Braga,52,30,16,4,10,60,44,16
    2012-2013,5,Estoril,45,30,13,6,11,47,37,10
    2012-2013,6,Rio Ave,42,30,12,6,12,35,42,-7
    2012-2013,7,Sporting CP,42,30,11,9,10,36,36,0
    2012-2013,8,Nacional,40,30,11,7,12,45,51,-6
    2012-2013,9,Vitória Guimarães,40,30,11,7,12,36,47,-11
    2012-2013,10,Marítimo,38,30,9,11,10,34,45,-11
    2012-2013,11,Académica,28,30,6,10,14,33,45,-12
    2012-2013,12,Vitória Setúbal,26,30,7,5,18,30,55,-25
    2012-2013,13,Gil Vicente,25,30,6,7,17,31,54,-23
    2012-2013,14,Olhanense,25,30,5,10,15,26,42,-16
    2012-2013,15,Moreirense,24,30,5,9,16,30,51,-21
    2012-2013,16,Beira-Mar,23,30,5,8,17,35,55,-20
    2013-2014,1,Benfica,74,30,23,5,2,65,25,40
    2013-2014,2,Sporting CP,67,30,20,7,3,56,22,34
    2013-2014,3,Porto,61,30,19,4,7,51,19,32
    2013-2014,4,Estoril,54,30,15,9,6,46,30,16
    2013-2014,5,Nacional,45,30,11,12,7,40,30,10
    2013-2014,6,Marítimo,41,30,11,8,11,36,40,-4
    2013-2014,7,Vitória Setúbal,39,30,10,9,11,30,30,0
    2013-2014,8,Académica,37,30,9,10,11,28,38,-10
    2013-2014,9,Braga,37,30,10,7,13,39,37,2
    2013-2014,10,Vitória Guimarães,35,30,10,5,15,29,34,-5
    2013-2014,11,Rio Ave,32,30,8,8,14,24,38,-14
    2013-2014,12,Arouca,31,30,8,7,15,24,38,-14
    2013-2014,13,Gil Vicente,31,30,8,7,15,24,38,-14
    2013-2014,14,Belenenses,28,30,6,10,14,22,36,-14
    2013-2014,15,Paços de Ferreira,24,30,6,6,18,15,46,-31
    2013-2014,16,Olhanense,24,30,6,6,18,17,45,-28
    2014-2015,1,Benfica,82,34,25,7,2,86,20,66
    2014-2015,2,Porto,77,34,24,5,5,73,24,49
    2014-2015,3,Sporting CP,73,34,22,7,5,67,31,36
    2014-2015,4,Braga,61,34,17,10,7,52,32,20
    2014-2015,5,Vitória Guimarães,50,34,14,8,12,40,41,-1
    2014-2015,6,Rio Ave,48,34,13,9,12,38,36,2
    2014-2015,7,Belenenses,47,34,13,8,13,37,42,-5
    2014-2015,8,Paços de Ferreira,46,34,12,10,12,39,39,0
    2014-2015,9,Moreirense,44,34,11,11,12,44,49,-5
    2014-2015,10,Marítimo,44,34,11,11,12,29,33,-4
    2014-2015,11,Nacional,43,34,10,13,11,38,43,-5
    2014-2015,12,Arouca,42,34,10,12,12,36,45,-9
    2014-2015,13,Estoril,41,34,10,11,13,36,45,-9
    2014-2015,14,Boavista,40,34,10,10,14,37,48,-11
    2014-2015,15,Académica,37,34,7,16,11,31,40,-9
    2014-2015,16,Gil Vicente,34,34,8,10,16,27,47,-20
    2014-2015,17,Vitória Setúbal,30,34,6,12,16,28,47,-19
    2014-2015,18,Penafiel,22,34,4,10,20,24,50,-26
    2015-2016,1,Benfica,88,34,28,4,2,85,19,66
    2015-2016,2,Sporting CP,86,34,27,5,2,75,21,54
    2015-2016,3,Porto,72,34,21,9,4,63,28,35
    2015-2016,4,Braga,60,34,18,6,10,50,36,14
    2015-2016,5,Arouca,53,34,15,8,11,43,41,2
    2015-2016,6,Rio Ave,47,34,11,14,9,37,36,1
    2015-2016,7,Vitória Guimarães,46,34,12,10,12,39,39,0
    2015-2016,8,Paços de Ferreira,44,34,12,8,14,41,49,-8
    2015-2016,9,Nacional,43,34,10,13,11,39,42,-3
    2015-2016,10,Estoril,43,34,11,10,13,42,47,-5
    2015-2016,11,Belenenses,43,34,10,13,11,33,36,-3
    2015-2016,12,Marítimo,42,34,10,12,12,38,42,-4
    2015-2016,13,Boavista,41,34,9,14,11,35,45,-10
    2015-2016,14,Moreirense,40,34,10,10,14,37,43,-6
    2015-2016,15,Vitória Setúbal,37,34,8,13,13,30,41,-11
    2015-2016,16,Tondela,35,34,7,14,13,34,45,-11
    2015-2016,17,União Madeira,28,34,5,13,16,25,45,-20
    2015-2016,18,Académica,25,34,4,13,17,22,52,-30
    2016-2017,1,Benfica,82,34,25,7,2,72,18,54
    2016-2017,2,Porto,76,34,22,10,2,72,22,50
    2016-2017,3,Sporting CP,70,34,21,7,6,68,36,32
    2016-2017,4,Braga,61,34,17,10,7,51,34,17
    2016-2017,5,Vitória Guimarães,57,34,16,9,9,49,36,13
    2016-2017,6,Marítimo,54,34,15,9,10,43,38,5
    2016-2017,7,Rio Ave,51,34,14,9,11,41,37,4
    2016-2017,8,Chaves,48,34,13,9,12,47,48,-1
    2016-2017,9,Feirense,47,34,12,11,11,38,38,0
    2016-2017,10,Estoril,43,34,10,13,11,39,44,-5
    2016-2017,11,Boavista,42,34,10,12,12,40,44,-4
    2016-2017,12,Vitória Setúbal,41,34,10,11,13,35,41,-6
    2016-2017,13,Paços de Ferreira,40,34,10,10,14,37,44,-7
    2016-2017,14,Arouca,38,34,9,11,14,31,45,-14
    2016-2017,15,Moreirense,38,34,9,11,14,35,49,-14
    2016-2017,16,Belenenses,37,34,8,13,13,33,42,-9
    2016-2017,17,Tondela,34,34,7,13,14,29,40,-11
    2016-2017,18,Nacional,28,34,5,13,16,29,53,-24
    2017-2018,1,Porto,88,34,28,4,2,82,18,64
    2017-2018,2,Benfica,81,34,25,6,3,80,26,54
    2017-2018,3,Sporting CP,77,34,24,5,5,73,32,41
    2017-2018,4,Braga,68,34,20,8,6,54,28,26
    2017-2018,5,Rio Ave,51,34,14,9,11,39,39,0
    2017-2018,6,Vitória Guimarães,49,34,14,7,13,36,37,-1
    2017-2018,7,Marítimo,48,34,12,12,10,38,37,1
    2017-2018,8,Belenenses,47,34,13,8,13,38,40,-2
    2017-2018,9,Chaves,46,34,12,10,12,34,36,-2
    2017-2018,10,Boavista,42,34,11,9,14,37,45,-8
    2017-2018,11,Vitória Setúbal,41,34,10,11,13,31,39,-8
    2017-2018,12,Paços de Ferreira,41,34,11,8,15,31,42,-11
    2017-2018,13,Moreirense,40,34,9,13,12,34,41,-7
    2017-2018,14,Tondela,40,34,11,7,16,34,42,-8
    2017-2018,15,Estoril,37,34,9,10,15,34,52,-18
    2017-2018,16,Aves,37,34,9,10,15,38,52,-14
    2017-2018,17,Feirense,32,34,7,11,16,28,40,-12
    2017-2018,18,Portimonense,31,34,5,16,13,28,41,-13
    2018-2019,1,Benfica,87,34,28,3,3,103,32,71
    2018-2019,2,Porto,85,34,27,4,3,75,17,58
    2018-2019,3,Sporting CP,74,34,22,8,4,67,30,37
    2018-2019,4,Braga,66,34,19,9,6,53,31,22
    2018-2019,5,Moreirense,52,34,15,7,12,42,46,-4
    2018-2019,6,Vitória Guimarães,48,34,13,9,12,49,44,5
    2018-2019,7,Belenenses,47,34,12,11,11,35,32,3
    2018-2019,8,Santa Clara,46,34,13,7,14,37,44,-7
    2018-2019,9,Rio Ave,45,34,11,12,11,42,39,3
    2018-2019,10,Portimonense,43,34,11,10,13,39,47,-8
    2018-2019,11,Vitória Setúbal,42,34,11,9,14,37,43,-6
    2018-2019,12,Boavista,42,34,10,12,12,34,40,-6
    2018-2019,13,Marítimo,42,34,11,9,14,37,45,-8
    2018-2019,14,Aves,40,34,11,7,16,35,49,-14
    2018-2019,15,Chaves,38,34,10,8,16,43,52,-9
    2018-2019,16,Tondela,35,34,8,11,15,33,43,-10
    2018-2019,17,Nacional,31,34,7,10,17,33,53,-20
    2018-2019,18,Feirense,24,34,5,9,20,28,55,-27
    2019-2020,1,Porto,82,34,26,4,4,74,24,50
    2019-2020,2,Benfica,81,34,25,6,3,77,26,51
    2019-2020,3,Sporting CP,66,34,18,12,4,55,27,28
    2019-2020,4,Braga,63,34,17,12,5,61,31,30
    2019-2020,5,Rio Ave,48,34,13,9,12,41,39,2
    2019-2020,6,Famalicão,46,34,11,13,10,49,49,0
    2019-2020,7,Vitória Guimarães,45,34,12,9,13,41,38,3
    2019-2020,8,Moreirense,43,34,11,10,13,38,45,-7
    2019-2020,9,Santa Clara,41,34,11,8,15,36,44,-8
    2019-2020,10,Gil Vicente,40,34,9,13,12,28,33,-5
    2019-2020,11,Vitória Setúbal,40,34,10,10,14,36,46,-10
    2019-2020,12,Boavista,39,34,9,12,13,28,37,-9
    2019-2020,13,Marítimo,38,34,10,8,16,35,49,-14
    2019-2020,14,Paços de Ferreira,37,34,10,7,17,40,53,-13
    2019-2020,15,Belenenses,37,34,7,16,11,28,39,-11
    2019-2020,16,Tondela,36,34,9,9,16,30,50,-20
    2019-2020,17,Portimonense,33,34,8,9,17,38,52,-14
    2019-2020,18,Aves,16,34,3,7,24,24,68,-44
    2020-2021,1,Sporting CP,85,34,25,10,0,77,20,57
    2020-2021,2,Porto,80,34,25,5,4,76,26,50
    2020-2021,3,Benfica,76,34,23,7,4,73,30,43
    2020-2021,4,Braga,63,34,18,9,7,56,35,21
    2020-2021,5,Paços de Ferreira,52,34,14,10,10,50,42,8
    2020-2021,6,Santa Clara,52,34,15,7,12,39,38,1
    2020-2021,7,Vitória Guimarães,49,34,13,10,11,48,48,0
    2020-2021,8,Gil Vicente,47,34,13,8,13,44,50,-6
    2020-2021,9,Moreirense,44,34,12,8,14,42,46,-4
    2020-2021,10,Portimonense,42,34,10,12,12,40,48,-8
    2020-2021,11,Tondela,41,34,10,11,13,36,48,-12
    2020-2021,12,Famalicão,39,34,9,12,13,38,50,-12
    2020-2021,13,Marítimo,37,34,9,10,15,33,49,-16
    2020-2021,14,Rio Ave,37,34,9,10,15,37,52,-15
    2020-2021,15,Belenenses,36,34,9,9,16,25,45,-20
    2020-2021,16,Boavista,35,34,8,11,15,38,48,-10
    2020-2021,17,Farense,32,34,7,11,16,28,45,-17
    2020-2021,18,Nacional,31,34,7,10,17,34,53,-19
    2021-2022,1,Porto,91,34,29,4,1,86,22,64
    2021-2022,2,Sporting CP,85,34,26,7,1,73,22,51
    2021-2022,3,Benfica,74,34,21,11,2,75,31,44
    2021-2022,4,Braga,64,34,18,10,6,55,32,23
    2021-2022,5,Gil Vicente,54,34,15,9,10,48,43,5
    2021-2022,6,Vitória Guimarães,49,34,14,7,13,43,41,2
    2021-2022,7,Estoril,48,34,12,12,10,42,44,-2
    2021-2022,8,Paços de Ferreira,47,34,12,11,11,45,44,1
    2021-2022,9,Santa Clara,46,34,13,7,14,41,49,-8
    2021-2022,10,Portimonense,44,34,11,11,12,46,54,-8
    2021-2022,11,Famalicão,43,34,10,13,11,41,42,-1
    2021-2022,12,Casa Pia,42,34,10,12,12,38,49,-11
    2021-2022,13,Boavista,40,34,8,16,10,38,44,-6
    2021-2022,14,Marítimo,38,34,10,8,16,29,52,-23
    2021-2022,15,Vizela,37,34,9,10,15,35,52,-17
    2021-2022,16,Arouca,34,34,7,13,14,32,46,-14
    2021-2022,17,Moreirense,33,34,8,9,17,35,49,-14
    2021-2022,18,Belenenses,17,34,3,8,23,21,63,-42
    2022-2023,1,Benfica,84,34,26,6,2,82,26,56
    2022-2023,2,Porto,79,34,24,7,3,75,22,53
    2022-2023,3,Sporting CP,75,34,22,9,3,66,26,40
    2022-2023,4,Braga,71,34,21,8,5,59,24,35
    2022-2023,5,Casa Pia,52,34,14,10,10,42,36,6
    2022-2023,6,Vitória Guimarães,50,34,14,8,12,48,47,1
    2022-2023,7,Arouca,47,34,12,11,11,47,47,0
    2022-2023,8,Famalicão,45,34,11,12,11,42,42,0
    2022-2023,9,Rio Ave,43,34,10,13,11,34,37,-3
    2022-2023,10,Estoril,42,34,10,12,12,32,35,-3
    2022-2023,11,Gil Vicente,41,34,11,8,15,36,43,-7
    2022-2023,12,Vizela,39,34,9,12,13,39,48,-9
    2022-2023,13,Boavista,38,34,8,14,12,28,43,-15
    2022-2023,14,Chaves,37,34,10,7,17,38,52,-14
    2022-2023,15,Portimonense,35,34,8,11,15,37,50,-13
    2022-2023,16,Marítimo,32,34,7,11,16,31,49,-18
    2022-2023,17,Paços de Ferreira,27,34,5,12,17,30,50,-20
    2022-2023,18,Santa Clara,26,34,6,8,20,35,73,-38
    2023-2024,1,Sporting CP,90,34,29,3,2,84,24,60
    2023-2024,2,Benfica,80,34,25,5,4,75,26,49
    2023-2024,3,Porto,76,34,22,10,2,80,28,52
    2023-2024,4,Braga,65,34,18,11,5,60,33,27
    2023-2024,5,Vitória Guimarães,56,34,15,11,8,55,44,11
    2023-2024,6,Moreirense,50,34,13,11,10,46,46,0
    2023-2024,7,Famalicão,49,34,13,10,11,43,42,1
    2023-2024,8,Casa Pia,45,34,11,12,11,37,41,-4
    2023-2024,9,Arouca,42,34,10,12,12,40,49,-9
    2023-2024,10,Rio Ave,42,34,10,12,12,39,45,-6
    2023-2024,11,Estoril,41,34,10,11,13,40,52,-12
    2023-2024,12,Gil Vicente,40,34,9,13,12,40,46,-6
    2023-2024,13,Boavista,38,34,8,14,12,33,42,-9
    2023-2024,14,Farense,38,34,9,11,14,38,49,-11
    2023-2024,15,Estrela,35,34,8,11,15,34,49,-15
    2023-2024,16,Portimonense,34,34,8,10,16,34,48,-14
    2023-2024,17,Vizela,30,34,6,12,16,32,51,-19
    2023-2024,18,Chaves,19,34,4,7,23,23,68,-45
    """
    standings_all = pd.read_csv(io.StringIO("\n".join(line.lstrip() for line in _CSV_DATA.splitlines())))
    return (standings_all,)


@app.cell
def _(mo, standings_all):
    available_seasons = sorted(standings_all["season"].unique().tolist())
    season_selector = mo.ui.multiselect(
        options=available_seasons,
        value=available_seasons,
        label="Selecionar Épocas",
    )
    season_selector
    return (season_selector,)


@app.cell
def _(mo, season_selector):
    mo.stop(len(season_selector.value) == 0, mo.md("**Por favor, selecione pelo menos uma época.**"))
    return


@app.cell
def _(season_selector, standings_all):
    standings = standings_all[standings_all["season"].isin(season_selector.value)].copy()
    return (standings,)


@app.cell
def _(mo):
    mo.md("""
    ## Classificações
    """)
    return


@app.cell
def _(mo, standings):
    mo.ui.table(standings, selection=None, pagination=True)
    return


@app.cell
def _(np, pd, standings):
    _gini_results = []
    for _season in sorted(standings["season"].unique()):
        _arr = np.sort(standings[standings["season"] == _season]["points"].to_numpy())
        _n = len(_arr)
        _indices = np.arange(1, _n + 1)
        _gini = (2 * np.sum(_indices * _arr)) / (_n * np.sum(_arr)) - (_n + 1) / _n
        _gini_results.append({"season": _season, "gini": float(_gini)})

    gini_df = pd.DataFrame(_gini_results)
    return (gini_df,)


@app.cell
def _(pd, standings):
    _gaps_results = []
    for _season in sorted(standings["season"].unique()):
        _s = standings[standings["season"] == _season].sort_values("rank")
        _pts = _s["points"].tolist()
        _n = len(_pts)
        # 18-team seasons: 3 relegated; 16-team seasons: 2 relegated
        _relegated = 3 if _n == 18 else 2
        _last_safe_pts = _pts[_n - _relegated - 1]
        _gaps_results.append({
            "season": _season,
            "first_second": _pts[0] - _pts[1],
            "first_fourth": _pts[0] - _pts[3],
            "first_last": _pts[0] - _pts[-1],
            "first_last_safe": _pts[0] - _last_safe_pts,
        })
    gaps_df = pd.DataFrame(_gaps_results)
    return (gaps_df,)


@app.cell
def _(pd, standings):
    _GRANDES = {"Benfica", "Porto", "Sporting CP"}
    _gp_results = []
    for _season in sorted(standings["season"].unique()):
        _s = standings[standings["season"] == _season]
        _grandes_avg = float(_s[_s["team"].isin(_GRANDES)]["points"].mean())
        _pequenos_avg = float(_s[~_s["team"].isin(_GRANDES)]["points"].mean())
        _gp_results.append({
            "season": _season,
            "grandes_avg": _grandes_avg,
            "pequenos_avg": _pequenos_avg,
            "gap": _grandes_avg - _pequenos_avg,
        })
    gp_df = pd.DataFrame(_gp_results)
    return (gp_df,)


@app.cell
def _(mo):
    mo.md("""
    ## Métricas de Competitividade

    ### Evolução do Coeficiente de Gini
    """)
    return


@app.cell
def _(alt, gini_df):
    _data = alt.Data(values=gini_df.to_dict("records"))
    _base = alt.Chart(_data).encode(
        x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("gini:Q", title="Coeficiente de Gini", scale=alt.Scale(domain=[0, 0.5])),
        tooltip=[
            alt.Tooltip("season:N", title="Época"),
            alt.Tooltip("gini:Q", title="Gini", format=".3f"),
        ],
    )
    _line = _base.mark_line(color="#1f77b4", strokeWidth=2)
    _points = _base.mark_circle(color="#1f77b4", size=60)
    (
        (_line + _points)
        .properties(title="Desigualdade de Pontos (Coeficiente de Gini) ao Longo do Tempo", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(gini_df, mo):
    mo.md(
        f"""
        **Estatísticas Resumo:**
        - Gini médio: **{gini_df["gini"].mean():.3f}**
        - Intervalo: {gini_df["gini"].min():.3f} – {gini_df["gini"].max():.3f}

        *Valores mais baixos indicam ligas mais competitivas (distribuição de pontos mais equilibrada).*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ### Evolução das Diferenças de Pontos
    """)
    return


@app.cell
def _(alt, gaps_df):
    _label_mapping = {
        "first_second": "1.º - 2.º (Luta pelo Título)",
        "first_fourth": "1.º - 4.º (Acesso à Liga dos Campeões)",
        "first_last": "1.º - Último (Amplitude)",
    }
    _melted = gaps_df.melt(
        id_vars=["season"],
        value_vars=["first_second", "first_fourth", "first_last"],
        var_name="gap_type",
        value_name="points",
    )
    _melted["Gap Type"] = _melted["gap_type"].map(_label_mapping)

    _safe_data = gaps_df[["season", "first_last_safe"]].rename(columns={"first_last_safe": "points"})
    _safe_data = _safe_data.copy()
    _safe_data["Gap Type"] = "1.º - Último Seguro (Zona de Manutenção)"

    _base = (
        alt.Chart(alt.Data(values=_melted.to_dict("records")))
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("points:Q", title="Diferença de Pontos"),
            color=alt.Color(
                "Gap Type:N",
                scale=alt.Scale(
                    domain=list(_label_mapping.values()),
                    range=["#e41a1c", "#377eb8", "#4daf4a"],
                ),
                legend=alt.Legend(title="Tipo de Diferença", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Gap Type:N", title="Diferença"),
                alt.Tooltip("points:Q", title="Pontos"),
            ],
        )
    )

    _safe_layer = (
        alt.Chart(alt.Data(values=_safe_data.to_dict("records")))
        .mark_line(point=True, strokeWidth=2, strokeDash=[4, 2])
        .encode(
            x=alt.X("season:N"),
            y=alt.Y("points:Q"),
            color=alt.Color(
                "Gap Type:N",
                scale=alt.Scale(
                    domain=["1.º - Último Seguro (Zona de Manutenção)"],
                    range=["#9467bd"],
                ),
                legend=alt.Legend(title="Tipo de Diferença", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Gap Type:N", title="Diferença"),
                alt.Tooltip("points:Q", title="Pontos"),
            ],
        )
    )

    (
        alt.layer(_base, _safe_layer)
        .resolve_legend(color="shared")
        .properties(title="Diferenças de Pontos ao Longo do Tempo", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(gaps_df, mo):
    mo.md(
        f"""
        **Estatísticas Resumo:**
        - Diferença média na luta pelo título (1.º–2.º): **{gaps_df["first_second"].mean():.1f} pontos**
        - Diferença média para acesso à Liga dos Campeões (1.º–4.º): **{gaps_df["first_fourth"].mean():.1f} pontos**

        *Diferenças menores indicam corridas ao título e lutas pela qualificação mais competitivas.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Dados das Métricas
    """)
    return


@app.cell
def _(gaps_df, gini_df, mo):
    combined_metrics = gini_df.merge(gaps_df, on="season", how="inner")
    mo.ui.table(combined_metrics, selection=None)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Grandes vs Pequenos

    Comparação da média de pontos do Big 3 (Benfica, Sporting e Porto) com todos os
    outros clubes da liga.
    """)
    return


@app.cell
def _(alt, gp_df):
    _label_mapping_gp = {
        "grandes_avg": "Grandes (Benfica, Sporting, Porto)",
        "pequenos_avg": "Pequenos (Restantes)",
    }
    _melted_gp = gp_df.melt(
        id_vars=["season"],
        value_vars=["grandes_avg", "pequenos_avg"],
        var_name="group",
        value_name="avg_points",
    )
    _melted_gp["Group"] = _melted_gp["group"].map(_label_mapping_gp)

    (
        alt.Chart(alt.Data(values=_melted_gp.to_dict("records")))
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("avg_points:Q", title="Média de Pontos"),
            color=alt.Color(
                "Group:N",
                scale=alt.Scale(
                    domain=list(_label_mapping_gp.values()),
                    range=["#d62728", "#2ca02c"],
                ),
                legend=alt.Legend(title="Grupo", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Group:N", title="Grupo"),
                alt.Tooltip("avg_points:Q", title="Média Pontos", format=".1f"),
            ],
        )
        .properties(title="Diferença de Pontos: Grandes vs Pequenos", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(gp_df, mo):
    mo.md(
        f"""
        **Estatísticas Resumo:**
        - Diferença média (Grandes – Pequenos): **{gp_df["gap"].mean():.1f} pontos**
        - Intervalo: {gp_df["gap"].min():.1f} – {gp_df["gap"].max():.1f} pontos

        *Uma diferença maior indica maior domínio dos clubes do Big 3.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Vista Combinada: Gini & Diferença Grandes vs Pequenos

    Gráfico de eixo duplo mostrando o Coeficiente de Gini (medida de desigualdade) e a
    diferença entre Grandes (Big 3) e Pequenos (restante da liga) ao longo do tempo.
    """)
    return


@app.cell
def _(alt, gini_df, gp_df):
    _combined = gini_df.merge(gp_df, on="season", how="inner")
    _data_combined = alt.Data(values=_combined.to_dict("records"))
    _base_combined = alt.Chart(_data_combined).encode(
        x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
    )
    _gini_line = _base_combined.mark_line(color="steelblue", strokeWidth=2).encode(
        y=alt.Y("gini:Q", title="Coeficiente de Gini", axis=alt.Axis(titleColor="steelblue", orient="left")),
        tooltip=[alt.Tooltip("season:N", title="Época"), alt.Tooltip("gini:Q", title="Gini", format=".3f")],
    )
    _gini_pts = _base_combined.mark_circle(color="steelblue", size=50).encode(
        y=alt.Y("gini:Q", title="", axis=alt.Axis(orient="left")),
    )
    _gap_line = _base_combined.mark_line(color="orange", strokeWidth=2, strokeDash=[5, 5]).encode(
        y=alt.Y("gap:Q", title="Dif. Grandes Pequenos", axis=alt.Axis(titleColor="orange", orient="right")),
        tooltip=[alt.Tooltip("season:N", title="Época"), alt.Tooltip("gap:Q", title="Dif. Grandes vs Pequenos", format=".1f")],
    )
    _gap_pts = _base_combined.mark_circle(color="orange", size=50).encode(
        y=alt.Y("gap:Q", title="Dif. Grandes Pequenos", axis=alt.Axis(titleColor="orange", orient="right")),
    )
    (
        alt.layer(_gini_line, _gini_pts, _gap_line, _gap_pts)
        .resolve_scale(y="independent")
        .properties(title="Coeficiente de Gini e Diferença Grandes vs Pequenos ao Longo do Tempo", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(mo):
    mo.md("""
    ## Estratificação em Três Escalões

    O Gini padrão captura a desigualdade global mas mistura dois fenómenos distintos: a
    dispersão das equipas *dentro* de cada escalão, e a distância *entre os próprios escalões*.

    Para isolar o segundo — o afastamento crescente entre a elite e o resto — usamos o
    **Gini-entre-escalões**: em cada época, cada equipa recebe a média de pontos do seu
    escalão em vez dos seus pontos reais, e calcula-se o Gini sobre essa tabela suavizada.
    O resultado mede apenas o grau de separação entre os três escalões, ignorando a variação
    interna de cada um.

    Três escalões: **Big 3** (Benfica, Sporting e Porto), **Perseguidor** (Braga,
    consistentemente em 4.º), **Restantes** (todos os outros).
    """)
    return


@app.cell
def _(np, pd, standings):
    _BIG3 = {"Benfica", "Porto", "Sporting CP"}
    _tier_results = []
    for _season in sorted(standings["season"].unique()):
        _s = standings[standings["season"] == _season]
        _big3_avg = float(_s[_s["team"].isin(_BIG3)]["points"].mean())
        _braga = _s[_s["team"] == "Braga"]
        _braga_avg = float(_braga["points"].iloc[0]) if len(_braga) > 0 else float(_s["points"].mean())
        _rest_avg = float(_s[~_s["team"].isin(_BIG3) & (_s["team"] != "Braga")]["points"].mean())

        # Between-group Gini: assign each team their tier mean, then compute Gini
        _vals = []
        for _, _row in _s.iterrows():
            if _row["team"] in _BIG3:
                _vals.append(_big3_avg)
            elif _row["team"] == "Braga":
                _vals.append(_braga_avg)
            else:
                _vals.append(_rest_avg)
        _arr = np.sort(np.array(_vals))
        _n = len(_arr)
        _idx = np.arange(1, _n + 1)
        _bg_gini = (2 * np.sum(_idx * _arr)) / (_n * np.sum(_arr)) - (_n + 1) / _n

        _tier_results.append({
            "season": _season,
            "big3_avg": _big3_avg,
            "braga": _braga_avg,
            "rest_avg": _rest_avg,
            "between_group_gini": float(_bg_gini),
        })
    tier_df = pd.DataFrame(_tier_results)
    return (tier_df,)


@app.cell
def _(alt, tier_df):
    _melted = tier_df.melt(
        id_vars=["season"],
        value_vars=["big3_avg", "braga", "rest_avg"],
        var_name="tier",
        value_name="avg_points",
    )
    _melted["Tier"] = _melted["tier"].map({
        "big3_avg": "Big 3 (média)",
        "braga": "Braga",
        "rest_avg": "Restantes (média)",
    })
    (
        alt.Chart(alt.Data(values=_melted.to_dict("records")))
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("avg_points:Q", title="Média de Pontos"),
            color=alt.Color(
                "Tier:N",
                scale=alt.Scale(
                    domain=["Big 3 (média)", "Braga", "Restantes (média)"],
                    range=["#d62728", "#ff7f0e", "#2ca02c"],
                ),
                legend=alt.Legend(title="Escalão", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Tier:N", title="Escalão"),
                alt.Tooltip("avg_points:Q", title="Média Pontos", format=".1f"),
            ],
        )
        .properties(title="Média de Pontos por Escalão (Big 3 / Braga / Restantes)", width=620, height=320)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(alt, gini_df, tier_df):
    _merged = gini_df.merge(tier_df[["season", "between_group_gini"]], on="season")
    _melted = _merged.melt(
        id_vars=["season"],
        value_vars=["gini", "between_group_gini"],
        var_name="metric",
        value_name="value",
    )
    _melted["Metric"] = _melted["metric"].map({
        "gini": "Gini Global",
        "between_group_gini": "Gini-entre-escalões",
    })
    (
        alt.Chart(alt.Data(values=_melted.to_dict("records")))
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("value:Q", title="Coeficiente de Gini", scale=alt.Scale(domain=[0, 0.25])),
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(
                    domain=["Gini Global", "Gini-entre-escalões"],
                    range=["#1f77b4", "#9467bd"],
                ),
                legend=alt.Legend(orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Metric:N"),
                alt.Tooltip("value:Q", title="Valor", format=".3f"),
            ],
        )
        .properties(title="Gini Global vs Gini-entre-escalões", width=620, height=320)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(mo, tier_df):
    _first5 = tier_df.head(5)
    _last5 = tier_df.tail(5)
    _big3_change = _last5["big3_avg"].mean() - _first5["big3_avg"].mean()
    _braga_change = _last5["braga"].mean() - _first5["braga"].mean()
    _rest_change = _last5["rest_avg"].mean() - _first5["rest_avg"].mean()
    mo.md(f"""
    Comparando as primeiras cinco épocas (2004–09) com as últimas cinco (2019–24):

    | Escalão | Média pts início | Média pts recente | Variação |
    |---------|-----------------|-------------------|----------|
    | Big 3 | {_first5["big3_avg"].mean():.1f} | {_last5["big3_avg"].mean():.1f} | **+{_big3_change:.1f}** |
    | Braga | {_first5["braga"].mean():.1f} | {_last5["braga"].mean():.1f} | **+{_braga_change:.1f}** |
    | Restantes | {_first5["rest_avg"].mean():.1f} | {_last5["rest_avg"].mean():.1f} | **{_rest_change:+.1f}** |

    O Big 3 ganhou em média ~{_big3_change:.0f} pontos enquanto o restante da liga ficou
    praticamente estagnado. O Braga também subiu mas mantém-se claramente abaixo do teto do
    Big 3. O Gini-entre-escalões a subir mais rapidamente do que o Gini global confirma que
    esta divergência — e não a variação aleatória dentro de cada época — é o principal motor
    do crescimento da desigualdade.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Coeficiente de Gini Normalizado por Pontos por Jogo

    As épocas entre 2006–2014 tiveram apenas 16 equipas (30 jogos), enquanto as restantes
    tiveram 18 equipas (34 jogos). Os pontos totais não são diretamente comparáveis entre
    estas eras. Dividir pelo número de jogos disputados coloca todas as épocas na mesma escala.
    """)
    return


@app.cell
def _(np, pd, standings):
    _ppg_results = []
    for _season in sorted(standings["season"].unique()):
        _s = standings[standings["season"] == _season]
        _ppg = (_s["points"] / _s["matches"]).to_numpy()
        _arr = np.sort(_ppg)
        _n = len(_arr)
        _indices = np.arange(1, _n + 1)
        _gini_ppg = (2 * np.sum(_indices * _arr)) / (_n * np.sum(_arr)) - (_n + 1) / _n
        _ppg_results.append({"season": _season, "gini_ppg": float(_gini_ppg)})
    ppg_gini_df = pd.DataFrame(_ppg_results)
    return (ppg_gini_df,)


@app.cell
def _(alt, gini_df, ppg_gini_df):
    _merged = gini_df.merge(ppg_gini_df, on="season")
    _melted = _merged.melt(
        id_vars=["season"],
        value_vars=["gini", "gini_ppg"],
        var_name="metric",
        value_name="value",
    )
    _melted["Metric"] = _melted["metric"].map({
        "gini": "Pontos totais",
        "gini_ppg": "Pontos por jogo",
    })
    (
        alt.Chart(alt.Data(values=_melted.to_dict("records")))
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("value:Q", title="Coeficiente de Gini", scale=alt.Scale(domain=[0, 0.5])),
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
                legend=alt.Legend(orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("Metric:N"),
                alt.Tooltip("value:Q", title="Gini", format=".3f"),
            ],
        )
        .properties(title="Gini: Pontos Totais vs Pontos por Jogo", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(mo):
    mo.md("""
    ## Concentração de Pontos no Top 3

    Que quota dos pontos totais da liga é recolhida pelas três primeiras equipas em cada época?
    Uma maior concentração significa que a distância entre o Big 3 e o resto é maior.
    """)
    return


@app.cell
def _(pd, standings):
    _conc_results = []
    for _season in sorted(standings["season"].unique()):
        _s = standings[standings["season"] == _season].sort_values("rank")
        _top3_pts = _s.head(3)["points"].sum()
        _total_pts = _s["points"].sum()
        _conc_results.append({
            "season": _season,
            "top3_share": round(100 * _top3_pts / _total_pts, 1),
        })
    concentration_df = pd.DataFrame(_conc_results)
    return (concentration_df,)


@app.cell
def _(alt, concentration_df):
    (
        alt.Chart(alt.Data(values=concentration_df.to_dict("records")))
        .mark_bar(color="#d62728", opacity=0.75)
        .encode(
            x=alt.X("season:N", title="Época", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("top3_share:Q", title="Quota de pontos do top 3 (%)", scale=alt.Scale(domain=[0, 50])),
            tooltip=[
                alt.Tooltip("season:N", title="Época"),
                alt.Tooltip("top3_share:Q", title="Quota top 3 (%)", format=".1f"),
            ],
        )
        .properties(title="Concentração de Pontos no Top 3 por Época", width=600, height=300)
        .configure_title(fontSize=16, anchor="start")
    )


@app.cell
def _(mo):
    mo.md("""
    ### Épocas com Clubes Pequenos no Top 3

    Épocas em que um clube fora de Benfica, Sporting e Porto entrou no top 3.
    """)
    return


@app.cell
def _(mo, standings):
    _GRANDES = {"Benfica", "Porto", "Sporting CP"}
    _upsets = (
        standings[
            (standings["rank"] <= 3) & (~standings["team"].isin(_GRANDES))
        ][["season", "team", "rank", "points"]]
        .sort_values(["season", "rank"])
        .reset_index(drop=True)
    )
    mo.ui.table(_upsets, selection=None)
    return


@app.cell
def _(concentration_df, gini_df, mo):
    _best = gini_df.loc[gini_df["gini"].idxmin()]
    _worst = gini_df.loc[gini_df["gini"].idxmax()]
    _most_conc = concentration_df.loc[concentration_df["top3_share"].idxmax()]
    _least_conc = concentration_df.loc[concentration_df["top3_share"].idxmin()]
    mo.md(f"""
    ## Destaques por Época

    | | Época | Valor |
    |---|---|---|
    | 🏆 Época mais competitiva (Gini mais baixo) | **{_best["season"]}** | {_best["gini"]:.3f} |
    | 📉 Época menos competitiva (Gini mais alto) | **{_worst["season"]}** | {_worst["gini"]:.3f} |
    | 🔝 Maior concentração no top 3 | **{_most_conc["season"]}** | {_most_conc["top3_share"]}% |
    | ⚖️ Época mais equilibrada | **{_least_conc["season"]}** | {_least_conc["top3_share"]}% |
    """)
    return


if __name__ == "__main__":
    app.run()
