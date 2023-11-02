-- 	Comandos SQL usandos no DBeaver

-- CREATE TABLE BILLBOARD E DEPOIS IMPORTAR O CSV "charts.csv"
CREATE TABLE PUBLIC."Billboard" (
	"date" DATE NULL
	,"rank" int4 NULL
	,song VARCHAR(300) NULL
	,artist VARCHAR(300) NULL
	,"last-week" float8 NULL
	,"peak-rank" int4 NULL
	,"weeks-on-board" int4 NULL
	);


-- EXTRAIR DADOS DA TABELA BILLBOARD

-- Realizar contagem com limite de 100 linhas
SELECT count(*) AS quantidade
FROM PUBLIC."Billboard" limit 100;

-- Renomeando a tabela Billboard por t1
SELECT "date"
	,t1."rank"
	,t1.song
	,t1.artist
	,t1."last-week"
	,t1."peak-rank"
	,t1."weeks-on-board"
FROM PUBLIC."Billboard" AS t1 limit 100;


-- Filtrando quantas vezes as músicas do Chuck Berry apareceram na Billboard, aqui simulamos um erro sem o group by
SELECT 
	t1.song
	,t1.artist
FROM PUBLIC."Billboard" AS t1
where t1.artist = 'Chuck Berry'
;

-- Corrigindo o erro do group by
SELECT t1.artist
	,t1.song
	,count(*) AS "#song"
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist = 'Chuck Berry'
group by t1.artist, t1.song
order by "#song" desc;

-- Filtrando quantas vezes as músicas do Chuck Berry e do Frankie Vaughan apareceram na Billboard
SELECT t1.artist
	,t1.song
	,count(*) AS "#song"
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist = 'Chuck Berry' or t1.artist = 'Frankie Vaughan'
group by t1.artist, t1.song
order by "#song" desc;

-- Trabalhando com listas nas filtragens com o WHERE
SELECT t1.artist
	,t1.song
	,count(*) AS "#song"
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist in('Chuck Berry','Frankie Vaughan')
group by t1.artist, t1.song
order by "#song" desc;

-- Filtrando quantidades de vezes que artistas apareceram na tabela
SELECT 
	t1.artist
	,count(*) as qtd_artist
FROM PUBLIC."Billboard" AS t1
group by t1.artist
ORDER BY t1.artist;

-- Filtrando quantidades de vezes que as músicas apareceram na tabela
SELECT 
	t1.song
	,count(*) as qtd_song
FROM PUBLIC."Billboard" AS t1
group by t1.song
ORDER BY t1.song;


-- Com ou sem DISTINCT
-- A consulta retorna todos os registros da tabela "Billboard" sem eliminar duplicatas. Isso significa que se houver linhas na tabela com os mesmos valores nas colunas "artist" e "song", essas duplicatas serão incluídas no resultado.
SELECT 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song;

-- Com a cláusula DISTINCT, a consulta elimina as duplicatas do resultado. Isso significa que apenas combinações únicas de valores nas colunas "artist" e "song" serão retornadas. Se houver várias linhas com os mesmos valores nessas colunas, apenas uma delas será incluída no resultado.	
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song;

-- Adicionando na tabela os cálculos das quantidades de artistas e de mpusicas, trabalhando com o LEFT JOIN
SELECT t1.artist
	,t2.qtd_artist
	,t1.song
	,t3.qtd_song
FROM PUBLIC."Billboard" AS t1
LEFT JOIN (
	SELECT t1.artist
		,count(*) AS qtd_artist
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY t1.artist
	) AS t2 ON (t1.artist = t2.artist)
LEFT JOIN (
	SELECT t1.song
		,count(*) AS qtd_song
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY t1.song
	) AS t3 ON (t1.song = t3.song);

-- Mesma lógica só que trabalhando com CTE ao invés de deixar o scrip grande demais 
WITH cte_artist
AS (
	SELECT t1.artist
		,count(*) AS qtd_artist
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY t1.artist
	)
	,cte_song
AS (
	SELECT t1.song
		,count(*) AS qtd_song
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY t1.song
	)
SELECT DISTINCT t1.artist
	,t2.qtd_artist
	,t1.song
	,t3.qtd_song
FROM PUBLIC."Billboard" AS t1
LEFT JOIN cte_artist AS t2 ON (t1.artist = t2.artist)
LEFT JOIN cte_song AS t3 ON (t1.song = t3.song)
ORDER BY t1.artist
	,t1.song;

-- Window Function

-- Criando CTE e mostrando os valores distintos sem duplicados das variáveis artistas e músicas
-- A coluna "row_number" atribui um número sequencial único a cada linha da consulta resultante, ordenado por "artist" e "song". Isso significa que cada linha receberá um número sequencial único com base na ordem em que aparece na consulta.
-- A coluna "row_number_artist" atribui um número sequencial único a cada linha dentro de cada grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a contagem reinicia quando o valor de "artist" muda.
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,row_number() over(order by artist, song) as "row_number"
	,row_number() over(partition by artist order by artist, song) as "row_number_artist"
from cte_billboard

-- A coluna "rank" atribui um número de classificação a cada linha dentro de cada grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a classificação é reiniciada quando o valor de "artist" muda. As linhas dentro de cada grupo são classificadas com base na ordem de "artist" e "song".
-- A consulta final seleciona todas as colunas da CTE "cte_billboard" e a coluna calculada "rank".
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,rank() over(partition by artist order by artist, song) as "rank"
from cte_billboard

-- A coluna "lag_song" retorna o valor da coluna "song" da linha anterior dentro do mesmo grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a função "lag()" considera apenas as linhas dentro do mesmo grupo de "artist". A ordem das linhas dentro do grupo é determinada pela cláusula "ORDER BY artist, song".
-- A consulta final seleciona todas as colunas da CTE "cte_billboard" e a coluna calculada "lag_song".
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,lag(song, 1) over(partition by artist order by artist, song) as "lag_song"
from cte_billboard

-- A coluna "lead_song" retorna o valor da coluna "song" da linha seguinte dentro do mesmo grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a função "lead()" considera apenas as linhas dentro do mesmo grupo de "artist". A ordem das linhas dentro do grupo é determinada pela cláusula "ORDER BY artist, song".
-- A consulta final seleciona todas as colunas da CTE "cte_billboard" e a coluna calculada "lead_song".
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,lead(song, 1) over(partition by artist order by artist, song) as "lead_song"
from cte_billboard

-- A coluna "first_value" retorna o valor da coluna "song" da primeira linha dentro do mesmo grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a função "first_value()" considera apenas as linhas dentro do mesmo grupo de "artist". A ordem das linhas dentro do grupo é determinada pela cláusula "ORDER BY artist, song".
-- A consulta final seleciona todas as colunas da CTE "cte_billboard" e a coluna calculada "first_value".
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,first_value(song) over(partition by artist order by artist, song) as "first_value"
from cte_billboard

-- A coluna "last_song" retorna o valor da coluna "song" da última linha dentro do mesmo grupo de "artist". Isso é feito usando a cláusula "PARTITION BY artist", o que significa que a função "last_value()" considera apenas as linhas dentro do mesmo grupo de "artist". A ordem das linhas dentro do grupo é determinada pela cláusula "ORDER BY artist, song".
-- A cláusula "RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING" especifica que a função de janela deve considerar todas as linhas dentro do mesmo grupo de "artist", independentemente da sua posição em relação à linha atual.
-- A consulta final seleciona todas as colunas da CTE "cte_billboard" e a coluna calculada "last_song".
with cte_billboard as(
SELECT distinct 
	t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
ORDER BY t1.artist
	,t1.song
)
select *
	,last_value(song) over(partition by artist order by artist, song range between unbounded preceding and unbounded following) as "last_song"
from cte_billboard

-- WINDOW FUNCTION
--Uma função de janela (window function) no SQL é uma função analítica que é aplicada a um conjunto de 
--linhas de dados em uma consulta, com base em um "quadro" (window) específico de linhas. 
--Ela permite que você realize cálculos em um conjunto de linhas relacionadas a cada linha individualmente, 
--sem a necessidade de criar subconsultas ou uniões complexas.
-- A função de janela é geralmente usada com a cláusula OVER, que define o quadro (window) de linhas para 
--o qual a função é aplicada. Esse quadro pode ser definido de várias maneiras, 
--como ordenando as linhas em uma ordem específica ou agrupando-as de acordo com uma coluna específica.
WITH T (StyleID, ID, Nome)
AS (SELECT 1,1, 'Rhuan' UNION ALL
	SELECT 1,1, 'Andre' UNION ALL
	SELECT 1,2, 'Ana' UNION ALL
	SELECT 1,2, 'Maria' UNION ALL
	SELECT 1,3, 'Letícia' UNION ALL
	SELECT 1,3, 'Lari' UNION ALL
	SELECT 1,4, 'Edson' UNION ALL
	SELECT 1,4, 'Marcos' UNION ALL
	SELECT 1,5, 'Rhuan' UNION ALL
	SELECT 1,5, 'Lari' UNION ALL
	SELECT 1,6, 'Daisy' UNION ALL
	SELECT 1,6, 'João'
	)
SELECT *
	,ROW_NUMBER() OVER (PARTITION BY StyleID ORDER BY ID) AS "ROW_NUMBER"
	,RANK() OVER (PARTITION BY StyleID ORDER BY ID) AS "RANK"
	,DENSE_RANK() OVER (PARTITION BY StyleID ORDER BY ID) AS "DENSE_RANK"
	,PERCENT_RANK() OVER (PARTITION BY StyleID ORDER BY ID) AS "PERCENT_RANK"
	,CUME_DIST() OVER (PARTITION BY StyleID ORDER BY ID) AS "CUME_DIST"
	,CUME_DIST() OVER (PARTITION BY StyleID ORDER BY ID DESC) AS "CUME_DIST_DESC"
	,FIRST_VALUE(Nome) OVER (PARTITION BY StyleID ORDER BY ID) AS "FIRST_VALUE"
	,LAST_VALUE(Nome) OVER (PARTITION BY StyleID ORDER BY ID) AS "LAST_VALUE"
	,NTH_VALUE(Nome, 5) OVER (PARTITION BY StyleID ORDER BY ID) AS "NTH_VALUE"
	,NTILE(5) OVER (ORDER BY StyleID) AS "NTILE_5"
	,LAG(Nome, 1) OVER (ORDER BY ID) AS "LAG_NOME"
	,LEAD(Nome, 1) OVER (ORDER BY ID) AS "LEAD_NOME"
FROM T;
/*Este código SQL realiza uma série de cálculos analíticos em um conjunto de dados que está definido na expressão WITH (também conhecida como uma "tabela comum de expressão" ou CTE) e retorna os resultados desses cálculos em colunas separadas. Vou explicar as partes principais do código:

Definindo a CTE (Common Table Expression): A CTE chamada T é definida e contém uma série de registros com três colunas: StyleID, ID e Nome. Essa CTE é usada como entrada para os cálculos subsequentes.

Cláusula SELECT com Funções de Janela:

ROW_NUMBER() OVER (...) AS "ROW_NUMBER": Esta função de janela atribui um número de linha sequencial para cada registro dentro de cada partição definida pela coluna StyleID, com base na ordenação pela coluna ID.
RANK() OVER (...) AS "RANK": Esta função de janela atribui um ranking para cada registro dentro de cada partição definida pela coluna StyleID, com base na ordenação pela coluna ID. Valores iguais recebem o mesmo ranking, e a próxima posição recebe o próximo número.
DENSE_RANK() OVER (...) AS "DENSE_RANK": Similar ao RANK(), mas os valores iguais recebem o mesmo ranking e não há "buracos" nos números de classificação.
PERCENT_RANK() OVER (...) AS "PERCENT_RANK": Calcula a posição relativa de cada registro em relação ao total de registros na partição, expressa como uma porcentagem.
CUME_DIST() OVER (...) AS "CUME_DIST": Calcula a distribuição cumulativa de registros em relação à partição, expressa como uma porcentagem.
CUME_DIST() OVER (...) AS "CUME_DIST_DESC": Calcula a distribuição cumulativa de registros em relação à partição, mas ordenada de forma decrescente.
FIRST_VALUE(Nome) OVER (...) AS "FIRST_VALUE": Retorna o primeiro valor da coluna Nome em cada partição.
LAST_VALUE(Nome) OVER (...) AS "LAST_VALUE": Retorna o último valor da coluna Nome em cada partição.
NTH_VALUE(Nome, 5) OVER (...) AS "NTH_VALUE": Retorna o valor da coluna Nome na quinta posição em cada partição.
NTILE(5) OVER (...) AS "NTILE_5": Divide as linhas em cinco partes iguais (quintis) com base na coluna StyleID.
LAG e LEAD: As colunas "LAG_NOME" e "LEAD_NOME" usam as funções LAG() e LEAD() para acessar os valores da coluna Nome da linha anterior e da próxima linha, respectivamente, com base na ordenação pela coluna ID.

Essas funções de janela são usadas para realizar análises de classificação, agregação e cálculos relativos aos dados da CTE T com base nas partições definidas por StyleID. O resultado final da consulta será uma tabela que inclui todas as colunas originais da CTE T, juntamente com as colunas geradas pelas funções de janela mencionadas.*/

create table tb_web_site as (
WITH cte_dedup_artist
AS (
	SELECT "date"
		,t1."rank"
		,t1.artist
		,ROW_NUMBER() OVER (
			PARTITION BY artist ORDER BY artist
				,"date"
			) AS "dedup"
	FROM PUBLIC."Billboard" AS t1
	ORDER BY t1.artist
		,t1."date"
	)
SELECT "date"
	,t1."rank"
	,t1.artist
FROM cte_dedup_artist as t1
WHERE "dedup" = '1'
);

select * from tb_web_site;

CREATE TABLE tb_artist AS (
	SELECT "date"
	,t1."rank"
	,t1.artist 
	,t1.song
	FROM PUBLIC."Billboard" AS t1 
	where t1.artist = 'AC/DC'
	ORDER BY t1.artist, t1.song, t1."date"
);

drop table tb_artist;

select * from tb_artist;

create view vw_artist as (
WITH cte_dedup_artist
AS (
	SELECT "date"
		,t1."rank"
		,t1.artist
		,ROW_NUMBER() OVER (
			PARTITION BY artist ORDER BY artist
				,"date"
			) AS "dedup"
	FROM tb_artist AS t1
	ORDER BY t1.artist
		,t1."date"
	)
SELECT "date"
	,t1."rank"
	,t1.artist
FROM cte_dedup_artist as t1
WHERE "dedup" = '1'
);

select * from vw_artist;

insert into tb_artist (
	SELECT "date"
	,t1."rank"
	,t1.artist 
	,t1.song
	FROM PUBLIC."Billboard" AS t1 
	where t1.artist like 'Elvis%'
	ORDER BY t1.artist, t1.song, t1."date"
);

select * from vw_artist;

create view vw_song as (
WITH cte_dedup_artist
AS (
	SELECT "date"
		,t1."rank"
		,t1.artist
		,t1.song
		,ROW_NUMBER() OVER (
			PARTITION BY artist ORDER BY artist, song, "date") AS "dedup"
	FROM tb_artist AS t1
	ORDER BY t1.artist, t1.song, t1."date")
SELECT "date"
	,t1."rank"
	,t1.artist
	,t1.song
FROM cte_dedup_artist as t1
WHERE "dedup" = '1'
);

select * from vw_song;

insert into tb_artist (
	SELECT "date"
	,t1."rank"
	,t1.artist 
	,t1.song
	FROM PUBLIC."Billboard" AS t1 
	where t1.artist like 'Adele%'
	ORDER BY t1.artist, t1.song, t1."date"
);

select * from vw_song;
select * from vw_artist;