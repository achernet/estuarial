from __future__ import print_function, division, absolute_import

from sqlalchemy.sql import column, and_, or_
from arraymanagement.client import ArrayClient
from estuarial.browse.universe import Universe
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.munging import lower_columns

def ven_to_seccode(vencodes,ventype):
    """
    :param vencodes: list of vencodes
    :param ventype: QADirect ventype of supplied vencodes
    :return: df mapping vencode to seccode
    """
    conn = ArrayManagementClient()
    arr = conn.aclient['/ENTITYMANAGEMENT/allsecmap.yaml']
    df = arr.select(and_(arr.ventype == ventype, arr.vencode.in_(vencodes)))
    return df

def sec_to_vencode(seccodes, ventype, allranks=False):
    """
    :param seccodes: list of vencodes
    :param ventype: QADirect ventype of supplied vencodes
    :return: df mapping vencode to seccode
    """
    conn = ArrayManagementClient()
    arr = conn.aclient['/ENTITYMANAGEMENT/allsecmap.yaml']
    df = arr.select(and_(arr.ventype == ventype, arr.seccode.in_(seccodes)))

    return df

if __name__ == "__main__":
    vencodes = [1,52545,1000, 760]
    ventype = 33
    s = ven_to_seccode(vencodes, ventype)
    v = sec_to_vencode([760,100249791], 33)
    print(s)
    print(v)