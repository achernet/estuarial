IF  EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'trqa.CsLatestCurrencyCode'))
DROP VIEW trqa.CsLatestCurrencyCode
GO

CREATE VIEW trqa.CsLatestCurrencyCode AS
    SELECT gvkey, curcd FROM (
      SELECT a.*,
      ROW_NUMBER() OVER (PARTITION BY gvkey ORDER BY datadate DESC) AS rn
       FROM(
        SELECT gvkey, curcd, datadate FROM dbo.CsCoADesInd
        UNION
        SELECT gvkey, curcdq AS curcd, datadate FROM dbo.CsCoIDesInd
        UNION
        SELECT gvkey, curcd, datadate FROM dbo.CsICoADesInd
        UNION
        SELECT gvkey, curcdq AS curcd, datadate FROM dbo.CsICoIDesInd
        ) a 
    ) b WHERE rn = 1
GO

IF  EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'trqa.CsCurrency'))
DROP VIEW trqa.CsCurrency
GO

CREATE VIEW trqa.CsCurrency AS
    SELECT 
    	tocurm AS toCur
    , 	fromcurm AS fromCur
    , 	dataDate
    , 	exRate
    , 	currencyConversionType
    FROM
    (
        SELECT tocurm, fromcurm, datadate
        ,    EXRAT1M,  EXRAT2M,  EXRAT3M
        ,    EXRAT4M,  EXRAT5M,  EXRAT6M
        ,    EXRAT7M,  EXRAT8M,  EXRAT9M
        ,    EXRAT10M, EXRAT11M, EXRAT12M
        ,    EXRAT13M, EXRAT14M, EXRAT15M
        ,    EXRAT16M, EXRAT17M, EXRAT18M
        ,    EXRATM
        FROM dbo.CSExRtMth
    ) pvt
    UNPIVOT
    (
        exRate FOR currencyConversionType IN (EXRAT1M, EXRAT2M,EXRAT3M,EXRAT4M,EXRAT5M,EXRAT6M,EXRAT7M,
                            EXRAT8M,EXRAT9M,EXRAT10M,EXRAT11M,EXRAT12M,EXRAT13M,EXRAT14M,
                            EXRAT15M,EXRAT16M,EXRAT17M,EXRAT18M,EXRATM)
    ) AS unpvt

    UNION ALL

    SELECT 
    		tocurd
    	, 	fromcurd
    	,	datadate
    	,	exRatd
    	,	'EXRATD'
    FROM dbo.CSExRTDly
GO



IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'trqa.getCompustatFundamentals') AND type in (N'P', N'PC'))
DROP PROCEDURE trqa.getCompustatFundamentals
GO
CREATE PROCEDURE trqa.getCompustatFundamentals
               
                   	 @gvkey XML
                ,    @number INT
                ,    @adj_value BIT = 1
                ,    @indfmt SMALLINT = 5
                ,    @datafmt SMALLINT = 2
                ,    @consol SMALLINT = 6
                ,    @toCur VARCHAR(5) = null
                ,    @convType VARCHAR(20) = 'exrat1m'
               
 AS 

 BEGIN

    SET NOCOUNT ON

    IF (@toCur = 'NULL')
        SET @toCur = NULL

    IF EXISTS (SELECT 1 WHERE object_id('tempdb.dbo.#fndData') IS NOT NULL)
        DROP TABLE #fndData
    IF EXISTS (SELECT 1 WHERE object_id('tempdb.dbo.#venCodes') IS NOT NULL)
        DROP TABLE #venCodes

    SELECT T.item.query('.').value('.', 'int') AS gvkey
    INTO #venCodes
    FROM @gvkey.nodes('venCodes/venCode') AS T(item)

    CREATE CLUSTERED INDEX IX ON #venCodes(gvkey)

    SELECT *
    INTO #fndData
    FROM
    (
        SELECT f.*
        FROM
        (
            SELECT f.gvkey, 204 AS group_, f.item, f.item AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsCoAFnd1 f
            INNER JOIN dbo.CSCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number < 1000

            UNION ALL

            SELECT f.gvkey, 233 AS group_, f.item, f.item AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsBkCoAFnd1 f
            INNER JOIN dbo.CSBkCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSBkCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number < 1000

            UNION ALL

            SELECT f.gvkey, 204 AS group_, f.item, f.item AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsICoAFnd1 f
            INNER JOIN dbo.CSICoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSICoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number < 1000

            UNION ALL

            SELECT f.gvkey, 233 AS group_, f.item, f.item AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsIBkCoAFnd1 f
            INNER JOIN dbo.CSIBkCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSIBkCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number < 1000

            UNION ALL

            SELECT f.gvkey, 205 AS group_, f.item, f.item +  1000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsCoAFnd2 f
            INNER JOIN dbo.CSCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number BETWEEN 1000 AND 2000

            UNION ALL

            SELECT f.gvkey, 234 AS group_, f.item, f.item +  1000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsBkCoAFnd2 f
            INNER JOIN dbo.CSBkCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSBkCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number BETWEEN 1000 AND 2000

            UNION ALL

            SELECT f.gvkey, 205 AS group_, f.item, f.item +  1000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , d.ACCTSTD, d.ACQMETH, d.ADRR, d.AJEX, d.AJP, d.APDEDATE, d.BSPR, d.COMPST, d.CURNCD, d.CURRTR
                , d.CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsICoAFnd2 f
            INNER JOIN dbo.CSICoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSICoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number BETWEEN 1000 AND 2000

            UNION ALL

            SELECT f.gvkey, 234 AS group_, f.item, f.item +  1000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, d.CURCD, 'Annual' AS periodType
                , ACCTSTD, ACQMETH, ADRR, AJEX, AJP, APDEDATE, BSPR, COMPST, CURNCD, CURRTR
                , CURUSCN, FDATE, FYEAR, d.FYR, ISMOD, OGM, PDATE, PDDUR, SCF, SRC
                , STALT, UDPL, UPD, RDQ, FQTR, 0 AS FyrFlag
            FROM dbo.CsIBkCoAFnd2 f
            INNER JOIN dbo.CSIBkCoAdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            LEFT JOIN dbo.CSIBkCoIdesind d2
                ON f.gvkey = d2.gvkey
                AND f.datadate = d2.datadate
                AND f.datafmt = d2.datafmt
                AND f.indfmt = d2.indfmt
                AND f.consol = d2.consol
            WHERE @number BETWEEN 1000 AND 2000

            UNION ALL

            SELECT f.gvkey, 220 AS group_, f.item, f.item +  3000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Semi-Annual' AS periodType
                , d.ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSCoIFndSA f
            INNER JOIN dbo.CSCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 3000 AND 4000

            UNION ALL

            SELECT f.gvkey, 249 AS group_, f.item, f.item +  3000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Semi-Annual' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSBkCoIFndSA f
            INNER JOIN dbo.CSBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 3000 AND 4000

            UNION ALL

            SELECT f.gvkey, 220 AS group_, f.item, f.item +  3000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Semi-Annual' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR,FyrFlag
            FROM dbo.CSICoIFndSA f
            INNER JOIN dbo.CSICoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 3000 AND 4000

            UNION ALL

            SELECT f.gvkey, 249 AS group_, f.item, f.item +  3000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Semi-Annual' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSIBkCoIFndSA f
            INNER JOIN dbo.CSIBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 3000 AND 4000

            UNION ALL

            SELECT f.gvkey, 219 AS group_, f.item, f.item + 4000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'YTD' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSCoIFndYTD f
            INNER JOIN dbo.CSCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 4000 AND 5000

            UNION ALL

            SELECT f.gvkey, 248 AS group_, f.item, f.item + 4000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'YTD' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSBkCoIFndYTD f
            INNER JOIN dbo.CSBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 4000 AND 5000

            UNION ALL

            SELECT f.gvkey, 219 AS group_, f.item, f.item + 4000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'YTD' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSICoIFndYTD f
            INNER JOIN dbo.CSICoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 4000 AND 5000

            UNION ALL

            SELECT f.gvkey, 248 AS group_, f.item, f.item + 4000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'YTD' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSIBkCoIFndYTD f
            INNER JOIN dbo.CSIBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 4000 AND 5000

            UNION ALL

            SELECT f.gvkey, 218 AS group_, f.item, f.item + 2000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Quarterly' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSCoIFndQ f
            INNER JOIN dbo.CSCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 2000 AND 3000

            UNION ALL

            SELECT f.gvkey, 247 AS group_, f.item, f.item + 2000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Quarterly' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSBkCoIFndQ f
            INNER JOIN dbo.CSBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 2000 AND 3000

            UNION ALL

            SELECT f.gvkey, 218 AS group_, f.item, f.item + 2000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Quarterly' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSICoIFndQ f
            INNER JOIN dbo.CSICoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 2000 AND 3000

            UNION ALL

            SELECT f.gvkey, 247 AS group_, f.item, f.item + 2000 AS number, f.datadate, f.value_ AS value
                , f.INDFMT, f.DATAFMT, f.CONSOL, 1 AS adj_value, CURCDQ AS CURCD, 'Quarterly' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM dbo.CSIBkCoIFndQ f
            INNER JOIN dbo.CSIBkCoIdesind d
                ON f.gvkey = d.gvkey
                AND f.datadate = d.datadate
                AND f.datafmt = d.datafmt
                AND f.indfmt = d.indfmt
                AND f.consol = d.consol
            WHERE @number BETWEEN 2000 AND 3000

            UNION ALL

            SELECT y.gvkey, y.group_, y.item, y.item + 5000 AS number, y.datadate
                , CASE    WHEN d.fqtr = 1
                    THEN y.value_
                    ELSE y.value_ - (
                                    SELECT value_ FROM (SELECT * FROM cscoifndytd UNION SELECT * FROM csbkcoifndytd UNION SELECT * FROM csicoifndytd UNION SELECT * FROM csibkcoifndytd) ytd
                                    WHERE ytd.gvkey = y.gvkey AND ytd.indfmt = y.indfmt AND ytd.consol = y.consol AND ytd.datafmt = y.datafmt AND ytd.item = y.item AND ytd.fyrflag = 0
                                    AND    ytd.datadate = (
                                                        SELECT MAX(datadate) FROM (SELECT * FROM cscoifndytd UNION SELECT * FROM csbkcoifndytd UNION SELECT * FROM csicoifndytd UNION SELECT * FROM csibkcoifndytd) ydate
                                                        WHERE ydate.gvkey = y.gvkey AND ydate.item = y.item AND ydate.indfmt = y.indfmt AND ydate.consol = y.consol AND ydate.datafmt = y.datafmt AND datadate < y.datadate
                                                        )
                                    )
                    END AS value
                , y.INDFMT, y.DATAFMT, y.CONSOL,1 AS adj_value, CURCDQ AS CURCD, 'YTDASQ' AS periodType
                , ACCTSTDQ, NULL AS ACQMETHQ, ADRRQ, AJEXQ, AJPQ, APDEDATEQ, BSPRQ, COMPSTQ, CURNCDQ, CURRTRQ
                , CURUSCNQ, FDATEQ, FYEARQ, d.FYR, NULL AS ISMODQ, OGMQ, PDATEQ, NULL AS PDDURQ, SCFQ, SRCQ
                , STALTQ, NULL AS UDPLQ, UPDQ, RDQ, FQTR, FyrFlag
            FROM (SELECT 219 AS group_, * FROM cscoifndytd UNION SELECT 248 AS group_, * FROM csbkcoifndytd UNION SELECT 219 AS group_, * FROM csicoifndytd UNION SELECT 248 AS group_, * FROM csibkcoifndytd) y
            JOIN (SELECT * FROM cscoidesind UNION SELECT * FROM csbkcoidesind UNION SELECT * FROM csicoidesind UNION SELECT * FROM csibkcoidesind) d
                ON    d.gvkey = y.gvkey
                AND    d.datadate = y.datadate
                AND    d.indfmt = y.indfmt
                AND    d.consol = y.consol
                AND    d.datafmt = y.datafmt
            WHERE @number BETWEEN 5000 AND 6000
        ) f

    ) final
    WHERE EXISTS (SELECT 1 FROM #venCodes v WHERE v.gvkey = final.gvkey)
    AND number = @number
    AND (INDFMT = @indfmt)
    AND (DATAFMT = @datafmt)
    AND (CONSOL = @consol)



    UPDATE f
    SET value = CASE WHEN item.adjust = 2 THEN ROUND(f.value * COALESCE(a.adjex, 1), 2)
                        WHEN item.adjust = 3 THEN ROUND(f.value / COALESCE(a.adjex, 1), 2)
                        ELSE f.value
                        END
    FROM #fndData f
    LEFT JOIN (SELECT * FROM CsCoAdjfact UNION SELECT * FROM CsICoAdjfact) a
        ON a.gvkey = f.gvkey
        AND f.datadate BETWEEN a.effdate AND COALESCE(a.thrudate,GETDATE())
        AND a.adjex IS NOT null
    LEFT JOIN dbo.CsNaItem item
        ON item.number = f.item
        AND item.group_ = f.group_
    WHERE @adj_value = 1

    SELECT *
    FROM
    (
        SELECT
            CASE
                WHEN @toCur IS NOT NULL THEN (value / toCur.exRate) * FROMCur.exRate
                WHEN toCur.exRate IS NOT NULL THEN (value / toCur.exRate) * FROMCur.exRate
                ELSE value
            END AS finalValue
        ,    ISNULL(@toCur, latest.CURCD) AS finalCurrency
        ,    f.*
        ,    ROW_NUMBER() OVER (PARTITION BY f.gvkey, FYEAR, f.FQTR ORDER BY FyrFlag) AS derivedRN
        FROM #fndData f
        LEFT JOIN trqa.CsLatestCurrencyCode latest
                ON f.gvkey = latest.gvkey
        LEFT JOIN trqa.CsCurrency toCur
            ON toCur.toCur = f.CURCD
            AND toCur.datadate = (SELECT MAX(datadate) FROM trqa.CsCurrency c WHERE c.toCur = f.CurCD AND c.datadate <= f.datadate)
            AND toCur.currencyConversionType = @convType
        LEFT JOIN trqa.CsCurrency FROMCur
            ON FROMCur.FROMCur = toCur.FROMCur
            AND FROMCur.datadate = (SELECT MAX(datadate) FROM trqa.CsCurrency c WHERE  c.toCur = f.CurCD AND c.datadate <= f.datadate)
            AND FROMCur.currencyConversionType = @convType
            AND FROMCur.toCur = ISNULL(@toCur,latest.curcd)
        WHERE (EXISTS (SELECT 1 FROM trqa.csCurrency c WHERE
             c.toCur = @toCur AND @toCur IS NOT NULL)
             OR @toCur IS NULL
             )
    ) returnValues
    WHERE finalValue IS NOT NULL
    AND derivedRN = 1
    ORDER BY datadate
END


-- DECLARE @RC int
-- DECLARE @gvkey xml
-- DECLARE @number int
-- DECLARE @adj_value bit
-- DECLARE @indfmt smallint
-- DECLARE @datafmt smallint
-- DECLARE @consol smallint
-- DECLARE @toCur varchar(5)
-- DECLARE @convType varchar(20)

-- set @gvkey = '<venCodes><venCode>6066</venCode></venCodes>'
-- set @number = '2288'
-- set @adj_value = '1'
-- set @indfmt = '5'
-- set @datafmt = '2' 
-- set @consol = '6' 
-- set @convType = 'EXRAT1M' 

-- EXECUTE @RC = [qai].[trqa].[getCompustatFundamentals] 
--    @gvkey
--   ,@number
--   ,@adj_value
--   ,@indfmt
--   ,@datafmt
--   ,@consol
--   ,@toCur
--   ,@convType
-- GO


