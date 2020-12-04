# -*- coding: utf-8 -*-
# flake8: noqa
# PyXB bindings for NM:4f059617657cbf045796906b94fd6da476500108
# Generated 2020-12-04 11:57:02.887420 by PyXB version 1.2.6 using Python 2.7.12.final.0
# Namespace urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp

from __future__ import unicode_literals
import logging
_logger = logging.getLogger(__name__)

try:
    import pyxb
    import pyxb.binding
    import pyxb.binding.datatypes
    import pyxb.binding.saxer
    import io
    import pyxb.utils.utility
    import pyxb.utils.domutils
    import sys
    import pyxb.utils.six as _six
except ImportError as err:
    _logger.debug(err)

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:70bf34b8-361f-11eb-88e3-9cb6d0f47f3b')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
from . import _cm as _ImportedBinding__cm

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (_ImportedBinding__cm.DatoAN_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 14, 4)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.IVP18 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='IVP18', tag='IVP18')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (_ImportedBinding__cm.DatoNP_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 22, 4)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.n1 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_.n2 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_.n3 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON_.n4 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON_.n5 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON_.n6 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON_.n7 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON_.n8 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON_.n9 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON_.n11 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON_.n12 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON_.n13 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='13', tag='n13')
STD_ANON_.n14 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='14', tag='n14')
STD_ANON_.n15 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='15', tag='n15')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Intestazione_IVP_Type with content type ELEMENT_ONLY
class Intestazione_IVP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Intestazione_IVP_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Intestazione_IVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 11, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFornitura uses Python identifier CodiceFornitura
    __CodiceFornitura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura'), 'CodiceFornitura', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFornitura', False, pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 13, 3), )


    CodiceFornitura = property(__CodiceFornitura.value, __CodiceFornitura.set, None, None)


    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFiscaleDichiarante uses Python identifier CodiceFiscaleDichiarante
    __CodiceFiscaleDichiarante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante'), 'CodiceFiscaleDichiarante', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFiscaleDichiarante', False, pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 20, 3), )


    CodiceFiscaleDichiarante = property(__CodiceFiscaleDichiarante.value, __CodiceFiscaleDichiarante.set, None, None)


    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceCarica uses Python identifier CodiceCarica
    __CodiceCarica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica'), 'CodiceCarica', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceCarica', False, pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 21, 3), )


    CodiceCarica = property(__CodiceCarica.value, __CodiceCarica.set, None, None)


    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IdSistema uses Python identifier IdSistema
    __IdSistema = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdSistema'), 'IdSistema', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIdSistema', False, pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 41, 3), )


    IdSistema = property(__IdSistema.value, __IdSistema.set, None, None)

    _ElementMap.update({
        __CodiceFornitura.name() : __CodiceFornitura,
        __CodiceFiscaleDichiarante.name() : __CodiceFiscaleDichiarante,
        __CodiceCarica.name() : __CodiceCarica,
        __IdSistema.name() : __IdSistema
    })
    _AttributeMap.update({

    })
_module_typeBindings.Intestazione_IVP_Type = Intestazione_IVP_Type
Namespace.addCategoryObject('typeBinding', 'Intestazione_IVP_Type', Intestazione_IVP_Type)


Intestazione = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intestazione'), pyxb.binding.datatypes.anyType, location=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 10, 1))
Namespace.addCategoryObject('elementBinding', Intestazione.name().localName(), Intestazione)



Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura'), STD_ANON, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 13, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante'), _ImportedBinding__cm.DatoCF_Type, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 20, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica'), STD_ANON_, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 21, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdSistema'), _ImportedBinding__cm.DatoCF_Type, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 41, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 20, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 21, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 41, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura')), pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 13, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante')), pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 20, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica')), pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 21, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdSistema')), pyxb.utils.utility.Location('/home/p01/PycharmProjects/tyre-erp-oca-update/repositories/elvenstudiotmp/l10n-italy/account_vat_period_end_statement/data/ivp18/intestazioneIvp_2018_v1.xsd', 41, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Intestazione_IVP_Type._Automaton = _BuildAutomaton()

