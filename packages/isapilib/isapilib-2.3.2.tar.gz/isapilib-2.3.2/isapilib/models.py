from isapilib.base import models as base_models
from isapilib.mixin.cte import CteMixin
from isapilib.mixin.venta import VentaMixin
from isapilib.mixin.vin import VinMixin


class Almacen(base_models.BaseAlmacen):
    class Meta:
        managed = False
        db_table = 'Alm'


class Art(base_models.BaseArt):
    class Meta:
        managed = False
        db_table = 'Art'


class ArtExistenciaNeta(base_models.BaseArtExistenciaNeta):
    class Meta:
        managed = False
        db_table = 'ArtExistenciaNeta'


class Empresa(base_models.BaseEmpresa):
    class Meta:
        managed = False
        db_table = 'Empresa'


class Agente(base_models.BaseAgente):
    class Meta:
        managed = False
        db_table = 'Agente'


class Cte(base_models.BaseCte, CteMixin):
    class Meta:
        managed = False
        db_table = 'Cte'


class Sucursal(base_models.BaseSucursal):
    class Meta:
        managed = False
        db_table = 'Sucursal'


class Compra(base_models.BaseCompra):
    class Meta:
        managed = False
        db_table = 'Compra'


class Vin(base_models.BaseVin, VinMixin):
    class Meta:
        managed = False
        db_table = 'VIN'


class VinTipoAccesorio(base_models.BaseVinTipoAccesorio):
    class Meta:
        managed = False
        db_table = 'VinTipoAccesorio'


class SerieLote(base_models.BaseSerieLote):
    class Meta:
        managed = False
        db_table = 'SerieLote'


class VinAccesorio(base_models.BaseVinAccesorio):
    class Meta:
        managed = False
        db_table = 'VinAccesorio'


class Venta(base_models.BaseVenta, VentaMixin):
    class Meta:
        managed = False
        db_table = 'Venta'


class VentaD(base_models.BaseVentaD):
    class Meta:
        managed = False
        db_table = 'VentaD'
        unique_together = (('id', 'renglon', 'renglon_sub'),)


class TipoOrdenOperacion(base_models.BaseTipoOrdenOperacion):
    class Meta:
        managed = False
        db_table = 'CA_MapeoTipoOrdenOperacion'
        unique_together = (('interfaz', 'operacion_intelisis'),)


class MaestroTipoOrdenOperacion(base_models.BaseMaestroTipoOrdenOperacion):
    class Meta:
        managed = False
        db_table = 'CA_MaestroTipoOrdenOperacionporInterfaz'


class MensajeLista(base_models.BaseMensajeLista):
    class Meta:
        managed = False
        db_table = 'MensajeLista'


class VentaTraspasarArticulos(base_models.BaseVentaTraspasarArticulos):
    class Meta:
        managed = False
        db_table = 'VentaTraspasarArticulos'
        unique_together = (('venta', 'estacion', 'rid'),)


class FormaPagoTipo(base_models.BaseFormaPagoTipo):
    class Meta:
        managed = False
        db_table = 'FormaPagoTipo'


class ListaPreciosD(base_models.BaseListaPreciosD):
    class Meta:
        managed = False
        db_table = 'ListaPreciosD'
        unique_together = (('lista', 'moneda', 'articulo'),)


class ArtCosto(base_models.BaseArtCosto):
    class Meta:
        managed = False
        db_table = 'ArtCosto'
