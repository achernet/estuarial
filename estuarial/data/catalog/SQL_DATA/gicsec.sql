        SELECT S.ID
        ,   S.CUSIP
        ,   S.NAME
        ,   G.SUBIND AS GIC_CODE
        ,   C1.DESC_ AS SECTOR
        ,   C2.DESC_ AS GROUP_
        ,   C3.DESC_ AS INDUSTRY
        ,   C4.DESC_ AS SUBINDUSTRY
        ,   M.SECCODE
        FROM         DBO.SECMSTRX S
        JOIN     DBO.SECMAPX M
            ON  M.SECCODE = S.SECCODE
            AND M.VENTYPE = 18 -- S&P Gics Direct
            AND M.RANK = 1
        JOIN     DBO.SPGDGICS G
            ON  G.GVKEY = M.VENCODE
        JOIN     DBO.SPGCODE C1
            ON  C1.CODE = LEFT(G.SUBIND,2)
            AND C1.TYPE_ = 1 -- GICS Descriptions
        JOIN     DBO.SPGCODE C2
            ON  C2.CODE = LEFT(G.SUBIND,4)
            AND C2.TYPE_ = 1 -- GICS Descriptions
        JOIN     DBO.SPGCODE C3
            ON  C3.CODE = LEFT(G.SUBIND,6)
            AND C3.TYPE_ = 1 -- GICS Descriptions
        JOIN     DBO.SPGCODE C4
            ON  C4.CODE = G.SUBIND
            AND C4.TYPE_ = 1 -- GICS Descriptions
            WHERE S.TYPE_ = 1