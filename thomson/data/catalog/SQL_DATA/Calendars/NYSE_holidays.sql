SELECT 
	e.ExchCode,
	e.ExchAbbr,
	e.ExchName,
	d.code AS datetypecode,
	i.name AS datetypename,
	d.date_
FROM sdexchinfo_v e
JOIN sddates_v d
	ON e.ExchCode = d.ExchCode
JOIN sdinfo_v i
	ON i.Code = d.Code
WHERE d.code <> 289
AND e.ExchCode = 16
ORDER BY d.date_ ASC