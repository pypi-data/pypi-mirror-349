import os
import streamlit.components.v1 as components

_RELEASE = True  # Set to False during dev

if not _RELEASE:
    _component_func = components.declare_component(
        "custom_aggrid",
        url="http://localhost:3001",  # Frontend dev server
    )
else:
    build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
    # build_dir = os.path.join(os.path.dirname(__file__), "../frontend/build")
    _component_func = components.declare_component(
        "custom_aggrid",
        path=build_dir
    )


def custom_aggrid(
    data,
    column_defs,
    gridOptions=None,
    theme="streamlit",  # <- ADD THIS
    update_mode=["FILTER_CHANGED", "CELL_VALUE_CHANGED"],
    height=400,
    columns_state=None,
    custom_css=None,
    enable_enterprise_modules=False,
    license_key=None,
    filter_model=None,
    key=None
):
    return _component_func(
        data=data,
        columnDefs=column_defs,
        filterModel=filter_model,
        key=key,
        gridOptions=gridOptions,
        theme=theme,  # <- PASS TO FRONTEND
        update_mode=update_mode,
        height=height,
        columns_state=columns_state,
        custom_css=custom_css,
        enable_enterprise_modules=enable_enterprise_modules,
        license_key=license_key,
    )
