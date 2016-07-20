// Generated code for Python source for module 'IPython.core.excolors'
// created by Nuitka version 0.5.20

// This code is in part copyright 2016 Kay Hayen.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "nuitka/prelude.hpp"

#include "__helpers.hpp"

// The _module_IPython$core$excolors is a Python object pointer of module type.

// Note: For full compatibility with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module_IPython$core$excolors;
PyDictObject *moduledict_IPython$core$excolors;

// The module constants used
extern PyObject *const_tuple_str_plain_LightBG_tuple;
extern PyObject *const_str_plain_Yellow;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_Cyan;
extern PyObject *const_str_plain_Blue;
extern PyObject *const_str_plain_filename;
static PyObject *const_str_digest_0aaa7ae312e5935b531d09076bbc3a0c;
static PyObject *const_tuple_str_plain_ex_colors_str_plain_C_tuple;
extern PyObject *const_str_plain_lineno;
extern PyObject *const_str_plain_LightCyan;
extern PyObject *const_str_plain_TermColors;
static PyObject *const_str_digest_cb524543011ecbc7009de6fe735738f1;
extern PyObject *const_str_plain_ColorScheme;
extern PyObject *const_dict_empty;
static PyObject *const_str_plain_LightPurple;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_NoColor;
static PyObject *const_str_plain_ExceptionColors;
extern PyObject *const_str_plain_Green;
extern PyObject *const_str_plain_em;
extern PyObject *const_int_0;
extern PyObject *const_str_plain_val;
extern PyObject *const_str_plain_exception_colors;
extern PyObject *const_str_plain_excName;
extern PyObject *const_str_plain_Red;
extern PyObject *const_str_digest_a6bf0bc1f6c3430e0b7e9a870562ae4b;
extern PyObject *const_str_plain_LightBlue;
static PyObject *const_str_plain_Purple;
extern PyObject *const_str_plain_topline;
extern PyObject *const_str_plain_nameEm;
extern PyObject *const_str_digest_2896da4659c0e23f2fb0650cde4c9812;
extern PyObject *const_str_plain_vName;
extern PyObject *const_str_plain_Normal;
extern PyObject *const_str_plain_add_scheme;
static PyObject *const_tuple_065083042758d78efd3d1cf6c769fead_tuple;
extern PyObject *const_str_plain_line;
static PyObject *const_str_plain_ex_colors;
extern PyObject *const_str_plain_LightBG;
static PyObject *const_str_digest_86767938083adbd5a953d6ccd04a7b2b;
extern PyObject *const_str_plain_C;
extern PyObject *const_str_plain_valEm;
extern PyObject *const_tuple_empty;
static PyObject *const_str_plain_excolors;
extern PyObject *const_tuple_str_plain_NoColor_tuple;
extern PyObject *const_str_plain_linenoEm;
extern PyObject *const_str_plain_caret;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_digest_748cbaee40503e420cb56830345361d5;
extern PyObject *const_str_plain_name;
extern PyObject *const_str_plain_LightGreen;
extern PyObject *const_str_plain_White;
extern PyObject *const_str_plain_Linux;
extern PyObject *const_str_plain_ColorSchemeTable;
extern PyObject *const_str_plain_normalEm;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_filenameEm;
extern PyObject *const_str_plain_LightRed;
extern PyObject *const_tuple_str_plain_Linux_tuple;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_digest_0aaa7ae312e5935b531d09076bbc3a0c = UNSTREAM_STRING( &constant_bin[ 366816 ], 55, 0 );
    const_tuple_str_plain_ex_colors_str_plain_C_tuple = PyTuple_New( 2 );
    const_str_plain_ex_colors = UNSTREAM_STRING( &constant_bin[ 366871 ], 9, 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_ex_colors_str_plain_C_tuple, 0, const_str_plain_ex_colors ); Py_INCREF( const_str_plain_ex_colors );
    PyTuple_SET_ITEM( const_tuple_str_plain_ex_colors_str_plain_C_tuple, 1, const_str_plain_C ); Py_INCREF( const_str_plain_C );
    const_str_digest_cb524543011ecbc7009de6fe735738f1 = UNSTREAM_STRING( &constant_bin[ 366880 ], 679, 0 );
    const_str_plain_LightPurple = UNSTREAM_STRING( &constant_bin[ 367559 ], 11, 1 );
    const_str_plain_ExceptionColors = UNSTREAM_STRING( &constant_bin[ 367570 ], 15, 1 );
    const_str_plain_Purple = UNSTREAM_STRING( &constant_bin[ 367564 ], 6, 1 );
    const_tuple_065083042758d78efd3d1cf6c769fead_tuple = PyTuple_New( 3 );
    PyTuple_SET_ITEM( const_tuple_065083042758d78efd3d1cf6c769fead_tuple, 0, const_str_plain_ColorSchemeTable ); Py_INCREF( const_str_plain_ColorSchemeTable );
    PyTuple_SET_ITEM( const_tuple_065083042758d78efd3d1cf6c769fead_tuple, 1, const_str_plain_TermColors ); Py_INCREF( const_str_plain_TermColors );
    PyTuple_SET_ITEM( const_tuple_065083042758d78efd3d1cf6c769fead_tuple, 2, const_str_plain_ColorScheme ); Py_INCREF( const_str_plain_ColorScheme );
    const_str_digest_86767938083adbd5a953d6ccd04a7b2b = UNSTREAM_STRING( &constant_bin[ 367585 ], 24, 0 );
    const_str_plain_excolors = UNSTREAM_STRING( &constant_bin[ 367598 ], 8, 1 );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_IPython$core$excolors( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_51c1d38114ea9a38f4442209f6e14bcd;
static PyCodeObject *codeobj_19e91ced571b52b2edef714d9d26ad22;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_86767938083adbd5a953d6ccd04a7b2b );
    codeobj_51c1d38114ea9a38f4442209f6e14bcd = MAKE_CODEOBJ( module_filename_obj, const_str_plain_exception_colors, 15, const_tuple_str_plain_ex_colors_str_plain_C_tuple, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_19e91ced571b52b2edef714d9d26ad22 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_excolors, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_function_1_exception_colors_of_IPython$core$excolors(  );


// The module function definitions.
static PyObject *impl_function_1_exception_colors_of_IPython$core$excolors( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *var_ex_colors = NULL;
    PyObject *var_C = NULL;
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_args_element_name_1;
    PyObject *tmp_args_element_name_2;
    PyObject *tmp_args_element_name_3;
    PyObject *tmp_args_name_1;
    PyObject *tmp_args_name_2;
    PyObject *tmp_args_name_3;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    PyObject *tmp_called_name_4;
    PyObject *tmp_called_name_5;
    PyObject *tmp_called_name_6;
    PyObject *tmp_called_name_7;
    PyObject *tmp_dict_key_1;
    PyObject *tmp_dict_key_2;
    PyObject *tmp_dict_key_3;
    PyObject *tmp_dict_key_4;
    PyObject *tmp_dict_key_5;
    PyObject *tmp_dict_key_6;
    PyObject *tmp_dict_key_7;
    PyObject *tmp_dict_key_8;
    PyObject *tmp_dict_key_9;
    PyObject *tmp_dict_key_10;
    PyObject *tmp_dict_key_11;
    PyObject *tmp_dict_key_12;
    PyObject *tmp_dict_key_13;
    PyObject *tmp_dict_key_14;
    PyObject *tmp_dict_key_15;
    PyObject *tmp_dict_key_16;
    PyObject *tmp_dict_key_17;
    PyObject *tmp_dict_key_18;
    PyObject *tmp_dict_key_19;
    PyObject *tmp_dict_key_20;
    PyObject *tmp_dict_key_21;
    PyObject *tmp_dict_key_22;
    PyObject *tmp_dict_key_23;
    PyObject *tmp_dict_key_24;
    PyObject *tmp_dict_key_25;
    PyObject *tmp_dict_key_26;
    PyObject *tmp_dict_key_27;
    PyObject *tmp_dict_key_28;
    PyObject *tmp_dict_key_29;
    PyObject *tmp_dict_key_30;
    PyObject *tmp_dict_key_31;
    PyObject *tmp_dict_key_32;
    PyObject *tmp_dict_key_33;
    PyObject *tmp_dict_key_34;
    PyObject *tmp_dict_key_35;
    PyObject *tmp_dict_key_36;
    PyObject *tmp_dict_key_37;
    PyObject *tmp_dict_key_38;
    PyObject *tmp_dict_key_39;
    PyObject *tmp_dict_key_40;
    PyObject *tmp_dict_key_41;
    PyObject *tmp_dict_key_42;
    PyObject *tmp_dict_key_43;
    PyObject *tmp_dict_key_44;
    PyObject *tmp_dict_key_45;
    PyObject *tmp_dict_key_46;
    PyObject *tmp_dict_key_47;
    PyObject *tmp_dict_key_48;
    PyObject *tmp_dict_value_1;
    PyObject *tmp_dict_value_2;
    PyObject *tmp_dict_value_3;
    PyObject *tmp_dict_value_4;
    PyObject *tmp_dict_value_5;
    PyObject *tmp_dict_value_6;
    PyObject *tmp_dict_value_7;
    PyObject *tmp_dict_value_8;
    PyObject *tmp_dict_value_9;
    PyObject *tmp_dict_value_10;
    PyObject *tmp_dict_value_11;
    PyObject *tmp_dict_value_12;
    PyObject *tmp_dict_value_13;
    PyObject *tmp_dict_value_14;
    PyObject *tmp_dict_value_15;
    PyObject *tmp_dict_value_16;
    PyObject *tmp_dict_value_17;
    PyObject *tmp_dict_value_18;
    PyObject *tmp_dict_value_19;
    PyObject *tmp_dict_value_20;
    PyObject *tmp_dict_value_21;
    PyObject *tmp_dict_value_22;
    PyObject *tmp_dict_value_23;
    PyObject *tmp_dict_value_24;
    PyObject *tmp_dict_value_25;
    PyObject *tmp_dict_value_26;
    PyObject *tmp_dict_value_27;
    PyObject *tmp_dict_value_28;
    PyObject *tmp_dict_value_29;
    PyObject *tmp_dict_value_30;
    PyObject *tmp_dict_value_31;
    PyObject *tmp_dict_value_32;
    PyObject *tmp_dict_value_33;
    PyObject *tmp_dict_value_34;
    PyObject *tmp_dict_value_35;
    PyObject *tmp_dict_value_36;
    PyObject *tmp_dict_value_37;
    PyObject *tmp_dict_value_38;
    PyObject *tmp_dict_value_39;
    PyObject *tmp_dict_value_40;
    PyObject *tmp_dict_value_41;
    PyObject *tmp_dict_value_42;
    PyObject *tmp_dict_value_43;
    PyObject *tmp_dict_value_44;
    PyObject *tmp_dict_value_45;
    PyObject *tmp_dict_value_46;
    PyObject *tmp_dict_value_47;
    PyObject *tmp_dict_value_48;
    PyObject *tmp_frame_locals;
    PyObject *tmp_kw_name_1;
    PyObject *tmp_kw_name_2;
    PyObject *tmp_kw_name_3;
    PyObject *tmp_return_value;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_source_name_3;
    PyObject *tmp_source_name_4;
    PyObject *tmp_source_name_5;
    PyObject *tmp_source_name_6;
    PyObject *tmp_source_name_7;
    PyObject *tmp_source_name_8;
    PyObject *tmp_source_name_9;
    PyObject *tmp_source_name_10;
    PyObject *tmp_source_name_11;
    PyObject *tmp_source_name_12;
    PyObject *tmp_source_name_13;
    PyObject *tmp_source_name_14;
    PyObject *tmp_source_name_15;
    PyObject *tmp_source_name_16;
    PyObject *tmp_source_name_17;
    PyObject *tmp_source_name_18;
    PyObject *tmp_source_name_19;
    PyObject *tmp_source_name_20;
    PyObject *tmp_source_name_21;
    PyObject *tmp_source_name_22;
    PyObject *tmp_source_name_23;
    PyObject *tmp_source_name_24;
    PyObject *tmp_source_name_25;
    PyObject *tmp_source_name_26;
    PyObject *tmp_source_name_27;
    PyObject *tmp_source_name_28;
    PyObject *tmp_source_name_29;
    PyObject *tmp_source_name_30;
    PyObject *tmp_source_name_31;
    PyObject *tmp_source_name_32;
    PyObject *tmp_source_name_33;
    PyObject *tmp_source_name_34;
    PyObject *tmp_source_name_35;
    PyObject *tmp_source_name_36;
    PyObject *tmp_source_name_37;
    PyObject *tmp_source_name_38;
    PyObject *tmp_source_name_39;
    PyObject *tmp_source_name_40;
    PyObject *tmp_source_name_41;
    PyObject *tmp_source_name_42;
    PyObject *tmp_source_name_43;
    PyObject *tmp_source_name_44;
    PyObject *tmp_source_name_45;
    PyObject *tmp_source_name_46;
    PyObject *tmp_source_name_47;
    PyObject *tmp_source_name_48;
    PyObject *tmp_source_name_49;
    PyObject *tmp_source_name_50;
    PyObject *tmp_source_name_51;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    static PyFrameObject *cache_frame_function = NULL;

    PyFrameObject *frame_function;

    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_function, codeobj_51c1d38114ea9a38f4442209f6e14bcd, module_IPython$core$excolors );
    frame_function = cache_frame_function;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_function );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    Py_INCREF( frame_function );
    assert( Py_REFCNT( frame_function ) == 2 ); // Frame stack

#if PYTHON_VERSION >= 340
    frame_function->f_executing += 1;
#endif

    // Framed code:
    tmp_called_name_1 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorSchemeTable );

    if (unlikely( tmp_called_name_1 == NULL ))
    {
        tmp_called_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_ColorSchemeTable );
    }

    if ( tmp_called_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "ColorSchemeTable" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 40;
        goto frame_exception_exit_1;
    }

    frame_function->f_lineno = 40;
    tmp_assign_source_1 = CALL_FUNCTION_NO_ARGS( tmp_called_name_1 );
    if ( tmp_assign_source_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 40;
        goto frame_exception_exit_1;
    }
    assert( var_ex_colors == NULL );
    var_ex_colors = tmp_assign_source_1;

    tmp_assign_source_2 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_TermColors );

    if (unlikely( tmp_assign_source_2 == NULL ))
    {
        tmp_assign_source_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_TermColors );
    }

    if ( tmp_assign_source_2 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "TermColors" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 43;
        goto frame_exception_exit_1;
    }

    assert( var_C == NULL );
    Py_INCREF( tmp_assign_source_2 );
    var_C = tmp_assign_source_2;

    tmp_source_name_1 = var_ex_colors;

    tmp_called_name_2 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_add_scheme );
    if ( tmp_called_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 44;
        goto frame_exception_exit_1;
    }
    tmp_called_name_3 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorScheme );

    if (unlikely( tmp_called_name_3 == NULL ))
    {
        tmp_called_name_3 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_ColorScheme );
    }

    if ( tmp_called_name_3 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "ColorScheme" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 44;
        goto frame_exception_exit_1;
    }

    tmp_args_name_1 = const_tuple_str_plain_NoColor_tuple;
    tmp_kw_name_1 = _PyDict_NewPresized( 16 );
    tmp_dict_key_1 = const_str_plain_topline;
    tmp_source_name_2 = var_C;

    if ( tmp_source_name_2 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 47;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_1 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_NoColor );
    if ( tmp_dict_value_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 47;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_1, tmp_dict_value_1 );
    Py_DECREF( tmp_dict_value_1 );
    tmp_dict_key_2 = const_str_plain_filename;
    tmp_source_name_3 = var_C;

    if ( tmp_source_name_3 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 50;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_2 = LOOKUP_ATTRIBUTE( tmp_source_name_3, const_str_plain_NoColor );
    if ( tmp_dict_value_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 50;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_2, tmp_dict_value_2 );
    Py_DECREF( tmp_dict_value_2 );
    tmp_dict_key_3 = const_str_plain_lineno;
    tmp_source_name_4 = var_C;

    if ( tmp_source_name_4 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 51;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_3 = LOOKUP_ATTRIBUTE( tmp_source_name_4, const_str_plain_NoColor );
    if ( tmp_dict_value_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 51;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_3, tmp_dict_value_3 );
    Py_DECREF( tmp_dict_value_3 );
    tmp_dict_key_4 = const_str_plain_name;
    tmp_source_name_5 = var_C;

    if ( tmp_source_name_5 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 52;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_4 = LOOKUP_ATTRIBUTE( tmp_source_name_5, const_str_plain_NoColor );
    if ( tmp_dict_value_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 52;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_4, tmp_dict_value_4 );
    Py_DECREF( tmp_dict_value_4 );
    tmp_dict_key_5 = const_str_plain_vName;
    tmp_source_name_6 = var_C;

    if ( tmp_source_name_6 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 53;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_5 = LOOKUP_ATTRIBUTE( tmp_source_name_6, const_str_plain_NoColor );
    if ( tmp_dict_value_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 53;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_5, tmp_dict_value_5 );
    Py_DECREF( tmp_dict_value_5 );
    tmp_dict_key_6 = const_str_plain_val;
    tmp_source_name_7 = var_C;

    if ( tmp_source_name_7 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 54;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_6 = LOOKUP_ATTRIBUTE( tmp_source_name_7, const_str_plain_NoColor );
    if ( tmp_dict_value_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 54;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_6, tmp_dict_value_6 );
    Py_DECREF( tmp_dict_value_6 );
    tmp_dict_key_7 = const_str_plain_em;
    tmp_source_name_8 = var_C;

    if ( tmp_source_name_8 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 55;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_7 = LOOKUP_ATTRIBUTE( tmp_source_name_8, const_str_plain_NoColor );
    if ( tmp_dict_value_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 55;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_7, tmp_dict_value_7 );
    Py_DECREF( tmp_dict_value_7 );
    tmp_dict_key_8 = const_str_plain_normalEm;
    tmp_source_name_9 = var_C;

    if ( tmp_source_name_9 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 58;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_8 = LOOKUP_ATTRIBUTE( tmp_source_name_9, const_str_plain_NoColor );
    if ( tmp_dict_value_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 58;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_8, tmp_dict_value_8 );
    Py_DECREF( tmp_dict_value_8 );
    tmp_dict_key_9 = const_str_plain_filenameEm;
    tmp_source_name_10 = var_C;

    if ( tmp_source_name_10 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 59;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_9 = LOOKUP_ATTRIBUTE( tmp_source_name_10, const_str_plain_NoColor );
    if ( tmp_dict_value_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 59;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_9, tmp_dict_value_9 );
    Py_DECREF( tmp_dict_value_9 );
    tmp_dict_key_10 = const_str_plain_linenoEm;
    tmp_source_name_11 = var_C;

    if ( tmp_source_name_11 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 60;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_10 = LOOKUP_ATTRIBUTE( tmp_source_name_11, const_str_plain_NoColor );
    if ( tmp_dict_value_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 60;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_10, tmp_dict_value_10 );
    Py_DECREF( tmp_dict_value_10 );
    tmp_dict_key_11 = const_str_plain_nameEm;
    tmp_source_name_12 = var_C;

    if ( tmp_source_name_12 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 61;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_11 = LOOKUP_ATTRIBUTE( tmp_source_name_12, const_str_plain_NoColor );
    if ( tmp_dict_value_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 61;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_11, tmp_dict_value_11 );
    Py_DECREF( tmp_dict_value_11 );
    tmp_dict_key_12 = const_str_plain_valEm;
    tmp_source_name_13 = var_C;

    if ( tmp_source_name_13 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 62;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_12 = LOOKUP_ATTRIBUTE( tmp_source_name_13, const_str_plain_NoColor );
    if ( tmp_dict_value_12 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 62;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_12, tmp_dict_value_12 );
    Py_DECREF( tmp_dict_value_12 );
    tmp_dict_key_13 = const_str_plain_excName;
    tmp_source_name_14 = var_C;

    if ( tmp_source_name_14 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 65;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_13 = LOOKUP_ATTRIBUTE( tmp_source_name_14, const_str_plain_NoColor );
    if ( tmp_dict_value_13 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 65;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_13, tmp_dict_value_13 );
    Py_DECREF( tmp_dict_value_13 );
    tmp_dict_key_14 = const_str_plain_line;
    tmp_source_name_15 = var_C;

    if ( tmp_source_name_15 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 66;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_14 = LOOKUP_ATTRIBUTE( tmp_source_name_15, const_str_plain_NoColor );
    if ( tmp_dict_value_14 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 66;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_14, tmp_dict_value_14 );
    Py_DECREF( tmp_dict_value_14 );
    tmp_dict_key_15 = const_str_plain_caret;
    tmp_source_name_16 = var_C;

    if ( tmp_source_name_16 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 67;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_15 = LOOKUP_ATTRIBUTE( tmp_source_name_16, const_str_plain_NoColor );
    if ( tmp_dict_value_15 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 67;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_15, tmp_dict_value_15 );
    Py_DECREF( tmp_dict_value_15 );
    tmp_dict_key_16 = const_str_plain_Normal;
    tmp_source_name_17 = var_C;

    if ( tmp_source_name_17 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 68;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_16 = LOOKUP_ATTRIBUTE( tmp_source_name_17, const_str_plain_NoColor );
    if ( tmp_dict_value_16 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_kw_name_1 );

        exception_lineno = 68;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_1, tmp_dict_key_16, tmp_dict_value_16 );
    Py_DECREF( tmp_dict_value_16 );
    frame_function->f_lineno = 68;
    tmp_args_element_name_1 = CALL_FUNCTION( tmp_called_name_3, tmp_args_name_1, tmp_kw_name_1 );
    Py_DECREF( tmp_kw_name_1 );
    if ( tmp_args_element_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_2 );

        exception_lineno = 68;
        goto frame_exception_exit_1;
    }
    frame_function->f_lineno = 68;
    {
        PyObject *call_args[] = { tmp_args_element_name_1 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_2, call_args );
    }

    Py_DECREF( tmp_called_name_2 );
    Py_DECREF( tmp_args_element_name_1 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 68;
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    tmp_source_name_18 = var_ex_colors;

    if ( tmp_source_name_18 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "ex_colors" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 72;
        goto frame_exception_exit_1;
    }

    tmp_called_name_4 = LOOKUP_ATTRIBUTE( tmp_source_name_18, const_str_plain_add_scheme );
    if ( tmp_called_name_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 72;
        goto frame_exception_exit_1;
    }
    tmp_called_name_5 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorScheme );

    if (unlikely( tmp_called_name_5 == NULL ))
    {
        tmp_called_name_5 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_ColorScheme );
    }

    if ( tmp_called_name_5 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "ColorScheme" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 72;
        goto frame_exception_exit_1;
    }

    tmp_args_name_2 = const_tuple_str_plain_Linux_tuple;
    tmp_kw_name_2 = _PyDict_NewPresized( 16 );
    tmp_dict_key_17 = const_str_plain_topline;
    tmp_source_name_19 = var_C;

    if ( tmp_source_name_19 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 75;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_17 = LOOKUP_ATTRIBUTE( tmp_source_name_19, const_str_plain_LightRed );
    if ( tmp_dict_value_17 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 75;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_17, tmp_dict_value_17 );
    Py_DECREF( tmp_dict_value_17 );
    tmp_dict_key_18 = const_str_plain_filename;
    tmp_source_name_20 = var_C;

    if ( tmp_source_name_20 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 78;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_18 = LOOKUP_ATTRIBUTE( tmp_source_name_20, const_str_plain_Green );
    if ( tmp_dict_value_18 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 78;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_18, tmp_dict_value_18 );
    Py_DECREF( tmp_dict_value_18 );
    tmp_dict_key_19 = const_str_plain_lineno;
    tmp_source_name_21 = var_C;

    if ( tmp_source_name_21 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 79;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_19 = LOOKUP_ATTRIBUTE( tmp_source_name_21, const_str_plain_Green );
    if ( tmp_dict_value_19 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 79;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_19, tmp_dict_value_19 );
    Py_DECREF( tmp_dict_value_19 );
    tmp_dict_key_20 = const_str_plain_name;
    tmp_source_name_22 = var_C;

    if ( tmp_source_name_22 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 80;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_20 = LOOKUP_ATTRIBUTE( tmp_source_name_22, const_str_plain_Purple );
    if ( tmp_dict_value_20 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 80;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_20, tmp_dict_value_20 );
    Py_DECREF( tmp_dict_value_20 );
    tmp_dict_key_21 = const_str_plain_vName;
    tmp_source_name_23 = var_C;

    if ( tmp_source_name_23 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 81;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_21 = LOOKUP_ATTRIBUTE( tmp_source_name_23, const_str_plain_Cyan );
    if ( tmp_dict_value_21 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 81;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_21, tmp_dict_value_21 );
    Py_DECREF( tmp_dict_value_21 );
    tmp_dict_key_22 = const_str_plain_val;
    tmp_source_name_24 = var_C;

    if ( tmp_source_name_24 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 82;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_22 = LOOKUP_ATTRIBUTE( tmp_source_name_24, const_str_plain_Green );
    if ( tmp_dict_value_22 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 82;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_22, tmp_dict_value_22 );
    Py_DECREF( tmp_dict_value_22 );
    tmp_dict_key_23 = const_str_plain_em;
    tmp_source_name_25 = var_C;

    if ( tmp_source_name_25 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 83;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_23 = LOOKUP_ATTRIBUTE( tmp_source_name_25, const_str_plain_LightCyan );
    if ( tmp_dict_value_23 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 83;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_23, tmp_dict_value_23 );
    Py_DECREF( tmp_dict_value_23 );
    tmp_dict_key_24 = const_str_plain_normalEm;
    tmp_source_name_26 = var_C;

    if ( tmp_source_name_26 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 86;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_24 = LOOKUP_ATTRIBUTE( tmp_source_name_26, const_str_plain_LightCyan );
    if ( tmp_dict_value_24 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 86;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_24, tmp_dict_value_24 );
    Py_DECREF( tmp_dict_value_24 );
    tmp_dict_key_25 = const_str_plain_filenameEm;
    tmp_source_name_27 = var_C;

    if ( tmp_source_name_27 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 87;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_25 = LOOKUP_ATTRIBUTE( tmp_source_name_27, const_str_plain_LightGreen );
    if ( tmp_dict_value_25 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 87;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_25, tmp_dict_value_25 );
    Py_DECREF( tmp_dict_value_25 );
    tmp_dict_key_26 = const_str_plain_linenoEm;
    tmp_source_name_28 = var_C;

    if ( tmp_source_name_28 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 88;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_26 = LOOKUP_ATTRIBUTE( tmp_source_name_28, const_str_plain_LightGreen );
    if ( tmp_dict_value_26 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 88;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_26, tmp_dict_value_26 );
    Py_DECREF( tmp_dict_value_26 );
    tmp_dict_key_27 = const_str_plain_nameEm;
    tmp_source_name_29 = var_C;

    if ( tmp_source_name_29 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 89;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_27 = LOOKUP_ATTRIBUTE( tmp_source_name_29, const_str_plain_LightPurple );
    if ( tmp_dict_value_27 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 89;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_27, tmp_dict_value_27 );
    Py_DECREF( tmp_dict_value_27 );
    tmp_dict_key_28 = const_str_plain_valEm;
    tmp_source_name_30 = var_C;

    if ( tmp_source_name_30 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 90;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_28 = LOOKUP_ATTRIBUTE( tmp_source_name_30, const_str_plain_LightBlue );
    if ( tmp_dict_value_28 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 90;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_28, tmp_dict_value_28 );
    Py_DECREF( tmp_dict_value_28 );
    tmp_dict_key_29 = const_str_plain_excName;
    tmp_source_name_31 = var_C;

    if ( tmp_source_name_31 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 93;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_29 = LOOKUP_ATTRIBUTE( tmp_source_name_31, const_str_plain_LightRed );
    if ( tmp_dict_value_29 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 93;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_29, tmp_dict_value_29 );
    Py_DECREF( tmp_dict_value_29 );
    tmp_dict_key_30 = const_str_plain_line;
    tmp_source_name_32 = var_C;

    if ( tmp_source_name_32 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 94;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_30 = LOOKUP_ATTRIBUTE( tmp_source_name_32, const_str_plain_Yellow );
    if ( tmp_dict_value_30 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 94;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_30, tmp_dict_value_30 );
    Py_DECREF( tmp_dict_value_30 );
    tmp_dict_key_31 = const_str_plain_caret;
    tmp_source_name_33 = var_C;

    if ( tmp_source_name_33 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 95;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_31 = LOOKUP_ATTRIBUTE( tmp_source_name_33, const_str_plain_White );
    if ( tmp_dict_value_31 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 95;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_31, tmp_dict_value_31 );
    Py_DECREF( tmp_dict_value_31 );
    tmp_dict_key_32 = const_str_plain_Normal;
    tmp_source_name_34 = var_C;

    if ( tmp_source_name_34 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 96;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_32 = LOOKUP_ATTRIBUTE( tmp_source_name_34, const_str_plain_Normal );
    if ( tmp_dict_value_32 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_kw_name_2 );

        exception_lineno = 96;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_2, tmp_dict_key_32, tmp_dict_value_32 );
    Py_DECREF( tmp_dict_value_32 );
    frame_function->f_lineno = 96;
    tmp_args_element_name_2 = CALL_FUNCTION( tmp_called_name_5, tmp_args_name_2, tmp_kw_name_2 );
    Py_DECREF( tmp_kw_name_2 );
    if ( tmp_args_element_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_4 );

        exception_lineno = 96;
        goto frame_exception_exit_1;
    }
    frame_function->f_lineno = 96;
    {
        PyObject *call_args[] = { tmp_args_element_name_2 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_4, call_args );
    }

    Py_DECREF( tmp_called_name_4 );
    Py_DECREF( tmp_args_element_name_2 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 96;
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    tmp_source_name_35 = var_ex_colors;

    if ( tmp_source_name_35 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "ex_colors" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 100;
        goto frame_exception_exit_1;
    }

    tmp_called_name_6 = LOOKUP_ATTRIBUTE( tmp_source_name_35, const_str_plain_add_scheme );
    if ( tmp_called_name_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 100;
        goto frame_exception_exit_1;
    }
    tmp_called_name_7 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorScheme );

    if (unlikely( tmp_called_name_7 == NULL ))
    {
        tmp_called_name_7 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_ColorScheme );
    }

    if ( tmp_called_name_7 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "ColorScheme" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 100;
        goto frame_exception_exit_1;
    }

    tmp_args_name_3 = const_tuple_str_plain_LightBG_tuple;
    tmp_kw_name_3 = _PyDict_NewPresized( 16 );
    tmp_dict_key_33 = const_str_plain_topline;
    tmp_source_name_36 = var_C;

    if ( tmp_source_name_36 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 103;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_33 = LOOKUP_ATTRIBUTE( tmp_source_name_36, const_str_plain_Red );
    if ( tmp_dict_value_33 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 103;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_33, tmp_dict_value_33 );
    Py_DECREF( tmp_dict_value_33 );
    tmp_dict_key_34 = const_str_plain_filename;
    tmp_source_name_37 = var_C;

    if ( tmp_source_name_37 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 106;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_34 = LOOKUP_ATTRIBUTE( tmp_source_name_37, const_str_plain_LightGreen );
    if ( tmp_dict_value_34 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 106;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_34, tmp_dict_value_34 );
    Py_DECREF( tmp_dict_value_34 );
    tmp_dict_key_35 = const_str_plain_lineno;
    tmp_source_name_38 = var_C;

    if ( tmp_source_name_38 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 107;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_35 = LOOKUP_ATTRIBUTE( tmp_source_name_38, const_str_plain_LightGreen );
    if ( tmp_dict_value_35 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 107;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_35, tmp_dict_value_35 );
    Py_DECREF( tmp_dict_value_35 );
    tmp_dict_key_36 = const_str_plain_name;
    tmp_source_name_39 = var_C;

    if ( tmp_source_name_39 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 108;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_36 = LOOKUP_ATTRIBUTE( tmp_source_name_39, const_str_plain_LightPurple );
    if ( tmp_dict_value_36 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 108;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_36, tmp_dict_value_36 );
    Py_DECREF( tmp_dict_value_36 );
    tmp_dict_key_37 = const_str_plain_vName;
    tmp_source_name_40 = var_C;

    if ( tmp_source_name_40 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 109;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_37 = LOOKUP_ATTRIBUTE( tmp_source_name_40, const_str_plain_Cyan );
    if ( tmp_dict_value_37 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 109;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_37, tmp_dict_value_37 );
    Py_DECREF( tmp_dict_value_37 );
    tmp_dict_key_38 = const_str_plain_val;
    tmp_source_name_41 = var_C;

    if ( tmp_source_name_41 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 110;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_38 = LOOKUP_ATTRIBUTE( tmp_source_name_41, const_str_plain_LightGreen );
    if ( tmp_dict_value_38 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 110;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_38, tmp_dict_value_38 );
    Py_DECREF( tmp_dict_value_38 );
    tmp_dict_key_39 = const_str_plain_em;
    tmp_source_name_42 = var_C;

    if ( tmp_source_name_42 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 111;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_39 = LOOKUP_ATTRIBUTE( tmp_source_name_42, const_str_plain_Cyan );
    if ( tmp_dict_value_39 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 111;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_39, tmp_dict_value_39 );
    Py_DECREF( tmp_dict_value_39 );
    tmp_dict_key_40 = const_str_plain_normalEm;
    tmp_source_name_43 = var_C;

    if ( tmp_source_name_43 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 114;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_40 = LOOKUP_ATTRIBUTE( tmp_source_name_43, const_str_plain_Cyan );
    if ( tmp_dict_value_40 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 114;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_40, tmp_dict_value_40 );
    Py_DECREF( tmp_dict_value_40 );
    tmp_dict_key_41 = const_str_plain_filenameEm;
    tmp_source_name_44 = var_C;

    if ( tmp_source_name_44 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 115;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_41 = LOOKUP_ATTRIBUTE( tmp_source_name_44, const_str_plain_Green );
    if ( tmp_dict_value_41 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 115;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_41, tmp_dict_value_41 );
    Py_DECREF( tmp_dict_value_41 );
    tmp_dict_key_42 = const_str_plain_linenoEm;
    tmp_source_name_45 = var_C;

    if ( tmp_source_name_45 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 116;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_42 = LOOKUP_ATTRIBUTE( tmp_source_name_45, const_str_plain_Green );
    if ( tmp_dict_value_42 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 116;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_42, tmp_dict_value_42 );
    Py_DECREF( tmp_dict_value_42 );
    tmp_dict_key_43 = const_str_plain_nameEm;
    tmp_source_name_46 = var_C;

    if ( tmp_source_name_46 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 117;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_43 = LOOKUP_ATTRIBUTE( tmp_source_name_46, const_str_plain_Purple );
    if ( tmp_dict_value_43 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 117;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_43, tmp_dict_value_43 );
    Py_DECREF( tmp_dict_value_43 );
    tmp_dict_key_44 = const_str_plain_valEm;
    tmp_source_name_47 = var_C;

    if ( tmp_source_name_47 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 118;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_44 = LOOKUP_ATTRIBUTE( tmp_source_name_47, const_str_plain_Blue );
    if ( tmp_dict_value_44 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 118;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_44, tmp_dict_value_44 );
    Py_DECREF( tmp_dict_value_44 );
    tmp_dict_key_45 = const_str_plain_excName;
    tmp_source_name_48 = var_C;

    if ( tmp_source_name_48 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 121;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_45 = LOOKUP_ATTRIBUTE( tmp_source_name_48, const_str_plain_Red );
    if ( tmp_dict_value_45 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 121;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_45, tmp_dict_value_45 );
    Py_DECREF( tmp_dict_value_45 );
    tmp_dict_key_46 = const_str_plain_line;
    tmp_source_name_49 = var_C;

    if ( tmp_source_name_49 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 123;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_46 = LOOKUP_ATTRIBUTE( tmp_source_name_49, const_str_plain_Red );
    if ( tmp_dict_value_46 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 123;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_46, tmp_dict_value_46 );
    Py_DECREF( tmp_dict_value_46 );
    tmp_dict_key_47 = const_str_plain_caret;
    tmp_source_name_50 = var_C;

    if ( tmp_source_name_50 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 124;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_47 = LOOKUP_ATTRIBUTE( tmp_source_name_50, const_str_plain_Normal );
    if ( tmp_dict_value_47 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 124;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_47, tmp_dict_value_47 );
    Py_DECREF( tmp_dict_value_47 );
    tmp_dict_key_48 = const_str_plain_Normal;
    tmp_source_name_51 = var_C;

    if ( tmp_source_name_51 == NULL )
    {
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "C" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 125;
        goto frame_exception_exit_1;
    }

    tmp_dict_value_48 = LOOKUP_ATTRIBUTE( tmp_source_name_51, const_str_plain_Normal );
    if ( tmp_dict_value_48 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );
        Py_DECREF( tmp_kw_name_3 );

        exception_lineno = 125;
        goto frame_exception_exit_1;
    }
    PyDict_SetItem( tmp_kw_name_3, tmp_dict_key_48, tmp_dict_value_48 );
    Py_DECREF( tmp_dict_value_48 );
    frame_function->f_lineno = 125;
    tmp_args_element_name_3 = CALL_FUNCTION( tmp_called_name_7, tmp_args_name_3, tmp_kw_name_3 );
    Py_DECREF( tmp_kw_name_3 );
    if ( tmp_args_element_name_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_6 );

        exception_lineno = 125;
        goto frame_exception_exit_1;
    }
    frame_function->f_lineno = 125;
    {
        PyObject *call_args[] = { tmp_args_element_name_3 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_6, call_args );
    }

    Py_DECREF( tmp_called_name_6 );
    Py_DECREF( tmp_args_element_name_3 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 125;
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    tmp_return_value = var_ex_colors;

    if ( tmp_return_value == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "ex_colors" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 128;
        goto frame_exception_exit_1;
    }

    Py_INCREF( tmp_return_value );
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif
    // Put the previous frame back on top.
    popFrameStack();
#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );
    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif
    popFrameStack();
#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );
    goto try_return_handler_1;

    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif

    {
        bool needs_detach = false;

        if ( exception_tb == NULL )
        {
            exception_tb = MAKE_TRACEBACK( frame_function, exception_lineno );
            needs_detach = true;
        }
        else if ( exception_lineno != -1 )
        {
            PyTracebackObject *traceback_new = MAKE_TRACEBACK( frame_function, exception_lineno );
            traceback_new->tb_next = exception_tb;
            exception_tb = traceback_new;

            needs_detach = true;
        }

        if (needs_detach)
        {

            tmp_frame_locals = PyDict_New();
            if ( var_ex_colors )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_ex_colors,
                    var_ex_colors
                );

                assert( res == 0 );
            }

            if ( var_C )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_C,
                    var_C
                );

                assert( res == 0 );
            }



            detachFrame( exception_tb, tmp_frame_locals );
        }
    }

    popFrameStack();

#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_1_exception_colors_of_IPython$core$excolors );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( var_ex_colors );
    var_ex_colors = NULL;

    Py_XDECREF( var_C );
    var_C = NULL;

    goto function_return_exit;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_type_1 = exception_type;
    exception_keeper_value_1 = exception_value;
    exception_keeper_tb_1 = exception_tb;
    exception_keeper_lineno_1 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = -1;

    Py_XDECREF( var_ex_colors );
    var_ex_colors = NULL;

    Py_XDECREF( var_C );
    var_C = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_1_exception_colors_of_IPython$core$excolors );
    return NULL;

function_exception_exit:
    assert( exception_type );
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );

    return NULL;
    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}



static PyObject *MAKE_FUNCTION_function_1_exception_colors_of_IPython$core$excolors(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_1_exception_colors_of_IPython$core$excolors,
        const_str_plain_exception_colors,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_51c1d38114ea9a38f4442209f6e14bcd,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_IPython$core$excolors,
        const_str_digest_cb524543011ecbc7009de6fe735738f1
    );

    return result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_IPython$core$excolors =
{
    PyModuleDef_HEAD_INIT,
    "IPython.core.excolors",   /* m_name */
    NULL,                /* m_doc */
    -1,                  /* m_size */
    NULL,                /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#endif

#if PYTHON_VERSION >= 300
extern PyObject *metapath_based_loader;
#endif

// The exported interface to CPython. On import of the module, this function
// gets called. It has to have an exact function name, in cases it's a shared
// library export. This is hidden behind the MOD_INIT_DECL.

MOD_INIT_DECL( IPython$core$excolors )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_IPython$core$excolors );
    }
    else
    {
        _init_done = true;
    }
#endif

#ifdef _NUITKA_MODULE
    // In case of a stand alone extension module, need to call initialization
    // the init here because that's the first and only time we are going to get
    // called here.

    // Initialize the constant values used.
    _initBuiltinModule();
    createGlobalConstants();

    // Initialize the compiled types of Nuitka.
    PyType_Ready( &Nuitka_Generator_Type );
    PyType_Ready( &Nuitka_Function_Type );
    PyType_Ready( &Nuitka_Method_Type );
    PyType_Ready( &Nuitka_Frame_Type );
#if PYTHON_VERSION >= 350
    PyType_Ready( &Nuitka_Coroutine_Type );
    PyType_Ready( &Nuitka_CoroutineWrapper_Type );
#endif

#if PYTHON_VERSION < 300
    _initSlotCompare();
#endif
#if PYTHON_VERSION >= 270
    _initSlotIternext();
#endif

    patchBuiltinModule();
    patchTypeComparison();

    // Enable meta path based loader if not already done.
    setupMetaPathBasedLoader();

#if PYTHON_VERSION >= 300
    patchInspectModule();
#endif

#endif

    createModuleConstants();
    createModuleCodeObjects();

    // puts( "in initIPython$core$excolors" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_IPython$core$excolors = Py_InitModule4(
        "IPython.core.excolors",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_IPython$core$excolors = PyModule_Create( &mdef_IPython$core$excolors );
#endif

    moduledict_IPython$core$excolors = (PyDictObject *)((PyModuleObject *)module_IPython$core$excolors)->md_dict;

    CHECK_OBJECT( module_IPython$core$excolors );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_a6bf0bc1f6c3430e0b7e9a870562ae4b, module_IPython$core$excolors );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module_IPython$core$excolors );

    if ( PyDict_GetItem( module_dict, const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

#ifndef __NUITKA_NO_ASSERT__
        int res =
#endif
            PyDict_SetItem( module_dict, const_str_plain___builtins__, value );

        assert( res == 0 );
    }

#if PYTHON_VERSION >= 330
    PyDict_SetItem( module_dict, const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_assign_source_4;
    PyObject *tmp_assign_source_5;
    PyObject *tmp_assign_source_6;
    PyObject *tmp_assign_source_7;
    PyObject *tmp_assign_source_8;
    PyObject *tmp_assign_source_9;
    PyObject *tmp_called_name_1;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_globals_2;
    PyObject *tmp_import_globals_3;
    PyObject *tmp_import_name_from_1;
    PyObject *tmp_import_name_from_2;
    PyObject *tmp_import_name_from_3;
    PyFrameObject *frame_module;


    // Module code.
    tmp_assign_source_1 = const_str_digest_0aaa7ae312e5935b531d09076bbc3a0c;
    UPDATE_STRING_DICT0( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = Py_None;
    UPDATE_STRING_DICT0( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_3 );
    tmp_assign_source_4 = const_str_digest_2896da4659c0e23f2fb0650cde4c9812;
    UPDATE_STRING_DICT0( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_4 );
    // Frame without reuse.
    frame_module = MAKE_MODULE_FRAME( codeobj_19e91ced571b52b2edef714d9d26ad22, module_IPython$core$excolors );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_module );
    assert( Py_REFCNT( frame_module ) == 1 );

#if PYTHON_VERSION >= 340
    frame_module->f_executing += 1;
#endif

    // Framed code:
    tmp_import_globals_1 = ((PyModuleObject *)module_IPython$core$excolors)->md_dict;
    frame_module->f_lineno = 13;
    tmp_import_name_from_1 = IMPORT_MODULE( const_str_digest_748cbaee40503e420cb56830345361d5, tmp_import_globals_1, tmp_import_globals_1, const_tuple_065083042758d78efd3d1cf6c769fead_tuple, const_int_0 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_5 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_ColorSchemeTable );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorSchemeTable, tmp_assign_source_5 );
    tmp_import_globals_2 = ((PyModuleObject *)module_IPython$core$excolors)->md_dict;
    frame_module->f_lineno = 13;
    tmp_import_name_from_2 = IMPORT_MODULE( const_str_digest_748cbaee40503e420cb56830345361d5, tmp_import_globals_2, tmp_import_globals_2, const_tuple_065083042758d78efd3d1cf6c769fead_tuple, const_int_0 );
    if ( tmp_import_name_from_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_6 = IMPORT_NAME( tmp_import_name_from_2, const_str_plain_TermColors );
    Py_DECREF( tmp_import_name_from_2 );
    if ( tmp_assign_source_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_TermColors, tmp_assign_source_6 );
    tmp_import_globals_3 = ((PyModuleObject *)module_IPython$core$excolors)->md_dict;
    frame_module->f_lineno = 13;
    tmp_import_name_from_3 = IMPORT_MODULE( const_str_digest_748cbaee40503e420cb56830345361d5, tmp_import_globals_3, tmp_import_globals_3, const_tuple_065083042758d78efd3d1cf6c769fead_tuple, const_int_0 );
    if ( tmp_import_name_from_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_7 = IMPORT_NAME( tmp_import_name_from_3, const_str_plain_ColorScheme );
    Py_DECREF( tmp_import_name_from_3 );
    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ColorScheme, tmp_assign_source_7 );
    tmp_assign_source_8 = MAKE_FUNCTION_function_1_exception_colors_of_IPython$core$excolors(  );
    UPDATE_STRING_DICT1( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_exception_colors, tmp_assign_source_8 );
    tmp_called_name_1 = GET_STRING_DICT_VALUE( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_exception_colors );

    if (unlikely( tmp_called_name_1 == NULL ))
    {
        tmp_called_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_exception_colors );
    }

    if ( tmp_called_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "exception_colors" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 135;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 135;
    tmp_assign_source_9 = CALL_FUNCTION_NO_ARGS( tmp_called_name_1 );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 135;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$excolors, (Nuitka_StringObject *)const_str_plain_ExceptionColors, tmp_assign_source_9 );

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_module );
#endif
    popFrameStack();

    assertFrameObject( frame_module );
    Py_DECREF( frame_module );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_module );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_module, exception_lineno );
    }
    else if ( exception_tb->tb_frame != frame_module )
    {
        PyTracebackObject *traceback_new = MAKE_TRACEBACK( frame_module, exception_lineno );
        traceback_new->tb_next = exception_tb;
        exception_tb = traceback_new;
    }

    // Put the previous frame back on top.
    popFrameStack();

#if PYTHON_VERSION >= 340
    frame_module->f_executing -= 1;
#endif
    Py_DECREF( frame_module );

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;

    return MOD_RETURN_VALUE( module_IPython$core$excolors );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
