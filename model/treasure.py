from model.finance import RF


class TD(RF):
    def __init__(self, itens, venc):
        super().__init__(self)
        self.__itens = [(it[0], it[1], it[2]) for it in self.itens]  # tuplas com (quantidade, preco, start)
        self.__venc = venc

    @property
    def vals_inv(self):
        return list(it[0] * it[1] for it in self.__itens)

    @property
    def val_inv(self):
        return sum(self.vals_inv)

    @property
    def dur(self):
        return [dt.date.today() - it[2] for it in self.__itens]

    @property
    def resta(self):
        return (self.venc - dt.date.today()).days / 365

    @property
    def imposto(self):
        return [self.imp(self.dur[i]) for i in range(len(self.__itens))]

    @property
    def taxes(self):
        return list(it[0] * it[1] * ((1 + 0.0025) ** ((dt.date.today() - it[2]).days / 365) - 1) for it in self.__itens)


class TDprefix(TD):
    def __init__(self, itens, jur, venc):
        super().__init__(self, itens, venc)
        self.__jur = jur
        # [ ( quant , preco , start ) ]

    @property
    def jur(self):
        return self.__jur

    @jur.setter
    def jur(self, jr):
        self.__jur = jr

    @property
    def preco(self):
        return -pv(fv=1000, nper=self.resta, rate=self.jur, pmt=0)

    @property
    def vals_brt(self):
        return list(self.preco * q[0] for q in self.__itens)

    @property
    def val_brt(self):
        return sum(it[0] for it in self.__itens) * self.preco

    @property
    def vals_liq(self):
        return list(self.vals_brt[i] - (self.vals_brt[i] - self.vals_inv[i]) * self.imp[i] - self.taxes[i])

    @property
    def val_liq(self):
        return sum(self.vals_liq)


pval = 44000  # Valor atual
saq = 20e3  # Renda mensal na aposentadoria
ja = 0.07  # Taxa anual média
jm = (1 + ja) ** (1 / 12) - 1
apos = 5e6  # Valor necessário para aposentar
n = (65 - 30) * 12
pmt = round(-pmt(nper=n, rate=jm, pv=-pval, fv=apos, when='end'), 2)

val = [pv]
idade = 29
tempo = list(range((100 - idade) * 12))
invest = pmt  # Valor investido ao mês
saque = 30000  # Valor sacado ao mês na aposentadoria
t = 0
for i in list(range((100 - idade) * 12)):
    tempo[i] = tempo[i] / 12 + idade
    if i == 0:
        continue
    if i <= n:
        val.append(round(val[i - 1] * (1 + jm), 2) + invest)
    else:
        val.append(round(val[i - 1] * (1 + jm), 2) - saque)
        if val[i] < 0:
            val[i] = 0
            if t == 0 and val[i] < 0:
                ind = i - 1
                t = 1