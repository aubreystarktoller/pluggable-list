import pytest
from pluggable_list.constants import  CONTROL_ATTR, Hook


l = pytest.pluggable_list


basic_list_constructor_fixture = l.custom_baselist_class_fixture(
    'basic_list_constructor', tuple(),
)

callback_mixin_class_fixture = l.callback_mixin_class_fixture(
    'callback_mixin_class_constructor'
)

callback_attrs_fixture = l.callback_attrs_fixture('callback_attrs')


def test_single_parent_inheritance(callback_attrs, basic_list_constructor):
    parent_cls = basic_list_constructor()
    child_cls = type('test_list', (parent_cls,), callback_attrs)
    ctl = getattr(child_cls, CONTROL_ATTR)

    hook_map = [
        ('get', Hook.get),
        ('set', Hook.set),
        ('remove', Hook.remove),
        ('sort', Hook.sort),
        ('revert', Hook.revert),
        ('begin_operation', Hook.begin_operation),
        ('end_operation', Hook.end_operation),
    ]
    
    for name, const in hook_map:
        if name + '_cb' in callback_attrs:
            assert ctl.get_callback(const) == callback_attrs[name + '_cb']
        elif name in parent_cls.registered_callbacks:
            assert ctl.get_callback(const) == getattr(parent_cls, name + '_cb')
        else:
            with pytest.raises(AttributeError):
                getattr(child_cls, name + '_cb')


def test_single_parent_inheritance_with_only_inherited_callbacks(basic_list_constructor):
    parent_cls = basic_list_constructor()
    child_cls = type('test_list', (parent_cls,), {})
    ctl = getattr(child_cls, CONTROL_ATTR)

    hook_map = [
        ('get', Hook.get),
        ('set', Hook.set),
        ('remove', Hook.remove),
        ('sort', Hook.sort),
        ('revert', Hook.revert),
        ('begin_operation', Hook.begin_operation),
        ('end_operation', Hook.end_operation),
    ]
    
    for name, const in hook_map:
        if name in parent_cls.registered_callbacks:
            assert ctl.get_callback(const) == getattr(parent_cls, name + '_cb')
        else:
            with pytest.raises(AttributeError):
                getattr(child_cls, name + '_cb')


def test_multi_parent_inheritance_with_pure_inherited_callbacks(basic_list_constructor, callback_mixin_class_constructor):
    parent_cls = basic_list_constructor()
    callback_mixin = callback_mixin_class_constructor()

    child_cls = type('test_list', (callback_mixin, parent_cls,), {})
    ctl = getattr(child_cls, CONTROL_ATTR)

    hook_map = [
        ('get', Hook.get),
        ('set', Hook.set),
        ('remove', Hook.remove),
        ('sort', Hook.sort),
        ('revert', Hook.revert),
        ('begin_operation', Hook.begin_operation),
        ('end_operation', Hook.end_operation),
    ]
    
    for name, const in hook_map:
        if name in callback_mixin.registered_callbacks:
            assert ctl.get_callback(const) == getattr(callback_mixin, name + '_cb')
        elif name in parent_cls.registered_callbacks:
            assert ctl.get_callback(const) == getattr(parent_cls, name + '_cb')
        else:
            with pytest.raises(AttributeError):
                getattr(child_cls, name + '_cb')
