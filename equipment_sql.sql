select  
	  --count(monthend) ItemCount
	  MonthEnd
	, cb_mak
	, CB_DTO
	, CB_DTP
	, datediff(month, co.Date, t.monthEnd) MonthsOnOrder
	, datediff(month, co.Date, cp.Date) MonthsPromised
	--, datediff(month, cast(cb_dto as date), cast(monthend as date)) MonthsOnOrder
	--, DATEDIFF(month, cast(CB_DTP as date), cast(cb_dto as date)) MonthsPromised
	, ck_slg, code.Description
, case cb_sta 
	when 'o' then 'ordered'
	when 'p' then 'presold'
	else cb_sta
  end --, *
from ref.TurnTable t
	join s2.cgigrp@ x on t.cb_grp = x.ck_gco
	join s2.Group_Code code on code.Code = t.cb_grp
	join ref.calendar co on co.PFWDateInt = t.CB_DTO
	join ref.calendar cp on cp.PFWDateInt = t.CB_DTP
where CB_DTO is not null
	and CK_ATT = 'N'
	and ck_slg in ('VM', 'CE', 'AG')
	and cb_sta not in ('R', 'S', 'V')
	and MonthEnd >= '2014-12-31'
	and cb_mak in ('JD', 'VE')
order by MonthEnd, Description
--group by 
--cb_mak
--	, CB_DTO
--	, CB_DTP
--	, datediff(month, cast(cb_dto as date), cast(monthend as date)) 
--	, DATEDIFF(month, cast(CB_DTP as date), cast(cb_dto as date)) 
--	, ck_slg, code.Description
--	,case cb_sta 
--	when 'o' then 'ordered'
--	when 'p' then 'presold'
--	else cb_sta
--  end