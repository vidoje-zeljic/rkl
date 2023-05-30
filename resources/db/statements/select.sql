select datum, porucilac, artikal, count(1) as num, sum(bruto), sum(tara), sum(neto)
from izvestaj
where prevoznik = 'Rudnik kamena Likodra'
group by porucilac, datum, artikal
order by datum desc, porucilac