CREATE FUNCTION trqa.GetNumberOfPeriods(@PERLEN int, @PERLENCODE char, @PERTYPECODE int)
	RETURNS INT
	AS
	BEGIN
		DECLARE @NumMonths int;
		DECLARE @AvgWksPerMth float;
		DECLARE @MonthsPerPeriod int;
		DECLARE @NumPeriods int;
		
		SET @AvgWksPerMth = 4.34821428; -- 365.25 / 12 / 7 == 4.34821428
		SET @MonthsPerPeriod = CASE @PERTYPECODE
									WHEN 1 THEN 12 
									WHEN 2 THEN 3 
									WHEN 3 THEN 6
									WHEN 4 THEN 4
									WHEN 6 THEN 12
									END;
		SET @NumPeriods = CASE @PERLENCODE 
									WHEN 'M' THEN @PERLEN / @MONTHSPERPERIOD
									WHEN 'W' THEN ROUND(@PERLEN / @AvgWksPerMth, 0) / @MonthsPerPeriod
									END;
		RETURN(@NumPeriods);
	END
	GO

CREATE VIEW trqa.RkdStdFinValCal AS

     SELECT
			v.code
		,	v.item
        ,	CASE v.PerTypeCode
				WHEN 1 THEN 'A'		--Annual
				WHEN 2 THEN 'Q'		--Quarterly
				WHEN 3 THEN 'S'		--Semi-Annual
				WHEN 4 THEN 'T'		--Triannual
				WHEN 5 THEN 'I'		--Interim (other)
				WHEN 6 THEN 'IA'		--Interim Annual
				END AS PerType
        ,	p.fyr
        ,	isnull(p.interimno, 1) as SeqNo		--annual data points will be null
        ,	isnull(trqa.GetNumberOfPeriods(s.PerLen, s.PerLenCode, v.PerTypeCode),1) as numPeriods --number of periods this entry is stating (always null for BS items)
        ,	v.PerEndDt
        ,	s.SourceDt as ReleaseDt
        ,	CASE v.StmtTypeCode
				WHEN 1 THEN 'I'
				WHEN 2 THEN	'C'
				WHEN 3 THEN 'B'
				END AS StmtType
		,	v.value_
		,	c.desc_ as CurrCode --as recorded
    FROM dbo.RKDFndStdFinVal v
    INNER JOIN dbo.RkdFndStdStmt s
        ON    v.code = s.code
        and v.PerEndDt = s.PerEndDt
        and v.PerTypeCode = s.PerTypeCode
        and v.StmtDt = s.StmtDt
        and v.StmtTypeCode = s.StmtTypeCode
    INNER JOIN (SELECT code, PerEndDt, PerTypeCode, StmtDt, FinalFiling, OrigAnncDt, CurrConvToCode,
                CASE WHEN PerTypeCode > 1 THEN 5 ELSE 1 END as ModPerTypeCode
                FROM dbo.RKDFndStdPerFiling) AS f ON
        s.code = f.code
        and s.PerEndDt = f.PerEndDt
        and s.PerTypeCode = f.PerTypeCode
        and s.StmtDt = f.StmtDt
    INNER JOIN dbo.RKDFndStdPeriod p ON
        f.code = p.code
        and f.PerEndDt = p.PerEndDt
        and f.ModPerTypeCode = p.PerTypeCode
    INNER JOIN dbo.RKDFndCode c
    on f.currconvtocode = c.code
    and c.type_ = 58
    WHERE (Flash = 0 OR (Flash = 1 AND CompStmtCode = 1) OR FinalFiling = 1)
    GO
        
               
        --       select * from trqa.rkdstdfinvalcal
          --     where  code = 2523
                --and  item = 1
            --    order by fyr, seqno