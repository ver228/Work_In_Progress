// This file contains helper functions that are automatically created from
// templates.

#include "nuitka/prelude.hpp"

extern PyObject *callPythonFunction( PyObject *func, PyObject **args, int count );


PyObject *CALL_FUNCTION_WITH_ARGS1( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 1; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        Nuitka_FunctionObject *function = (Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 1 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 1; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 1 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 1 * sizeof(PyObject *) );
            memcpy( python_pars + 1, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 1 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        Nuitka_MethodObject *method = (Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 1 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 1; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 1 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 1 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 1, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 1 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called );

        if ( flags & METH_NOARGS )
        {
#if 1 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (1 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 1 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (1 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 1 );

            PyObject *result;

            assert( flags && METH_VARARGS );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            if ( flags && METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            1
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 1 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS2( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 2; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        Nuitka_FunctionObject *function = (Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 2 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 2; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 2 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 2 * sizeof(PyObject *) );
            memcpy( python_pars + 2, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 2 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        Nuitka_MethodObject *method = (Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 2 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 2; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 2 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 2 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 2, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 2 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called );

        if ( flags & METH_NOARGS )
        {
#if 2 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (2 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 2 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (2 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 2 );

            PyObject *result;

            assert( flags && METH_VARARGS );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            if ( flags && METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            2
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 2 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS3( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 3; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        Nuitka_FunctionObject *function = (Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 3 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 3; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 3 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 3 * sizeof(PyObject *) );
            memcpy( python_pars + 3, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 3 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        Nuitka_MethodObject *method = (Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 3 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 3; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 3 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 3 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 3, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 3 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called );

        if ( flags & METH_NOARGS )
        {
#if 3 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (3 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 3 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (3 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 3 );

            PyObject *result;

            assert( flags && METH_VARARGS );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            if ( flags && METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            3
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 3 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}
/* Code to register embedded modules for meta path based loading if any. */
#if 1 == 1

#include "nuitka/unfreezing.hpp"

/* Table for lookup to find compiled or bytecode modules included in this
 * binary or module, or put along this binary as extension modules. We do
 * our own loading for each of these.
 */
MOD_INIT_DECL( PyQt4 );
MOD_INIT_DECL( PyQt4$QtCore$$45$postLoad );
static struct Nuitka_MetaPathBasedLoaderEntry meta_path_loader_entries[] =
{
    { (char *)"PyQt4", MOD_INIT_NAME( PyQt4 ), NULL, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"PyQt4.QtCore", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"PyQt4.QtCore-postLoad", MOD_INIT_NAME( PyQt4$QtCore$$45$postLoad ), NULL, 0, NUITKA_COMPILED_MODULE },
    { (char *)"PyQt4.QtGui", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_bisect", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_bz2", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_cn", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_hk", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_iso2022", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_jp", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_kr", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_tw", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_crypt", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_csv", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_ctypes", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_curses", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_curses_panel", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_datetime", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_dbm", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_decimal", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_elementtree", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_gdbm", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_hashlib", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_heapq", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_json", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_lsprof", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_lzma", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_multibytecodec", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_multiprocessing", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_opcode", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_pickle", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_posixsubprocess", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_random", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_scproxy", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_socket", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_sqlite3", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_ssl", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_struct", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_tkinter", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"array", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"audioop", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"binascii", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"fcntl", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"grp", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"math", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"mmap", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"pyexpat", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"readline", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"resource", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"select", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"sip", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"termios", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"unicodedata", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"zlib", NULL, NULL, 0, NUITKA_SHLIB_FLAG },
    { (char *)"__future__", NULL, &constant_bin[ 516 ], 4360, NUITKA_BYTECODE_FLAG },
    { (char *)"_compression", NULL, &constant_bin[ 4876 ], 4490, NUITKA_BYTECODE_FLAG },
    { (char *)"_dummy_thread", NULL, &constant_bin[ 9366 ], 5102, NUITKA_BYTECODE_FLAG },
    { (char *)"_markupbase", NULL, &constant_bin[ 14468 ], 8946, NUITKA_BYTECODE_FLAG },
    { (char *)"_osx_support", NULL, &constant_bin[ 23414 ], 10526, NUITKA_BYTECODE_FLAG },
    { (char *)"_pyio", NULL, &constant_bin[ 33940 ], 75943, NUITKA_BYTECODE_FLAG },
    { (char *)"_sitebuiltins", NULL, &constant_bin[ 109883 ], 3710, NUITKA_BYTECODE_FLAG },
    { (char *)"_strptime", NULL, &constant_bin[ 113593 ], 15555, NUITKA_BYTECODE_FLAG },
    { (char *)"_sysconfigdata", NULL, &constant_bin[ 129148 ], 21135, NUITKA_BYTECODE_FLAG },
    { (char *)"_threading_local", NULL, &constant_bin[ 150283 ], 6976, NUITKA_BYTECODE_FLAG },
    { (char *)"aifc", NULL, &constant_bin[ 157259 ], 27742, NUITKA_BYTECODE_FLAG },
    { (char *)"argparse", NULL, &constant_bin[ 185001 ], 65561, NUITKA_BYTECODE_FLAG },
    { (char *)"asynchat", NULL, &constant_bin[ 250562 ], 8521, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio", NULL, &constant_bin[ 259083 ], 908, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"asyncio.base_events", NULL, &constant_bin[ 259991 ], 37125, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.base_subprocess", NULL, &constant_bin[ 297116 ], 9793, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.compat", NULL, &constant_bin[ 306909 ], 789, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.constants", NULL, &constant_bin[ 307698 ], 283, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.coroutines", NULL, &constant_bin[ 307981 ], 8658, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.events", NULL, &constant_bin[ 316639 ], 24171, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.futures", NULL, &constant_bin[ 340810 ], 15611, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.locks", NULL, &constant_bin[ 356421 ], 15690, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.log", NULL, &constant_bin[ 372111 ], 285, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.proactor_events", NULL, &constant_bin[ 372396 ], 17913, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.protocols", NULL, &constant_bin[ 390309 ], 6132, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.queues", NULL, &constant_bin[ 396441 ], 8933, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.selector_events", NULL, &constant_bin[ 405374 ], 30782, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.sslproto", NULL, &constant_bin[ 436156 ], 21215, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.streams", NULL, &constant_bin[ 457371 ], 16400, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.subprocess", NULL, &constant_bin[ 473771 ], 7145, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.tasks", NULL, &constant_bin[ 480916 ], 20977, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.test_utils", NULL, &constant_bin[ 501893 ], 16222, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.transports", NULL, &constant_bin[ 518115 ], 12178, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.unix_events", NULL, &constant_bin[ 530293 ], 31250, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncore", NULL, &constant_bin[ 561543 ], 17213, NUITKA_BYTECODE_FLAG },
    { (char *)"base64", NULL, &constant_bin[ 578756 ], 18210, NUITKA_BYTECODE_FLAG },
    { (char *)"bdb", NULL, &constant_bin[ 596966 ], 18600, NUITKA_BYTECODE_FLAG },
    { (char *)"binhex", NULL, &constant_bin[ 615566 ], 13468, NUITKA_BYTECODE_FLAG },
    { (char *)"bisect", NULL, &constant_bin[ 629034 ], 2875, NUITKA_BYTECODE_FLAG },
    { (char *)"bz2", NULL, &constant_bin[ 631909 ], 11825, NUITKA_BYTECODE_FLAG },
    { (char *)"cProfile", NULL, &constant_bin[ 643734 ], 4647, NUITKA_BYTECODE_FLAG },
    { (char *)"calendar", NULL, &constant_bin[ 648381 ], 27568, NUITKA_BYTECODE_FLAG },
    { (char *)"cgi", NULL, &constant_bin[ 675949 ], 29906, NUITKA_BYTECODE_FLAG },
    { (char *)"cgitb", NULL, &constant_bin[ 705855 ], 11051, NUITKA_BYTECODE_FLAG },
    { (char *)"chunk", NULL, &constant_bin[ 716906 ], 5260, NUITKA_BYTECODE_FLAG },
    { (char *)"cmd", NULL, &constant_bin[ 722166 ], 13449, NUITKA_BYTECODE_FLAG },
    { (char *)"code", NULL, &constant_bin[ 735615 ], 9867, NUITKA_BYTECODE_FLAG },
    { (char *)"codeop", NULL, &constant_bin[ 745482 ], 6495, NUITKA_BYTECODE_FLAG },
    { (char *)"colorsys", NULL, &constant_bin[ 751977 ], 3682, NUITKA_BYTECODE_FLAG },
    { (char *)"compileall", NULL, &constant_bin[ 755659 ], 8914, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent", NULL, &constant_bin[ 764573 ], 180, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"concurrent.futures", NULL, &constant_bin[ 764753 ], 728, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"concurrent.futures._base", NULL, &constant_bin[ 765481 ], 20956, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent.futures.process", NULL, &constant_bin[ 786437 ], 16389, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent.futures.thread", NULL, &constant_bin[ 802826 ], 3954, NUITKA_BYTECODE_FLAG },
    { (char *)"configparser", NULL, &constant_bin[ 806780 ], 48213, NUITKA_BYTECODE_FLAG },
    { (char *)"contextlib", NULL, &constant_bin[ 854993 ], 10956, NUITKA_BYTECODE_FLAG },
    { (char *)"copy", NULL, &constant_bin[ 865949 ], 8162, NUITKA_BYTECODE_FLAG },
    { (char *)"crypt", NULL, &constant_bin[ 874111 ], 2469, NUITKA_BYTECODE_FLAG },
    { (char *)"csv", NULL, &constant_bin[ 876580 ], 12969, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes", NULL, &constant_bin[ 889549 ], 17561, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"ctypes._endian", NULL, &constant_bin[ 907110 ], 2108, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes.macholib", NULL, &constant_bin[ 909218 ], 351, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"ctypes.macholib.dyld", NULL, &constant_bin[ 909569 ], 4753, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes.macholib.dylib", NULL, &constant_bin[ 914322 ], 2117, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes.macholib.framework", NULL, &constant_bin[ 916439 ], 2416, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes.util", NULL, &constant_bin[ 918855 ], 7135, NUITKA_BYTECODE_FLAG },
    { (char *)"curses", NULL, &constant_bin[ 925990 ], 1966, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"curses.ascii", NULL, &constant_bin[ 927956 ], 4264, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.has_key", NULL, &constant_bin[ 932220 ], 4815, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.panel", NULL, &constant_bin[ 937035 ], 275, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.textpad", NULL, &constant_bin[ 937310 ], 6322, NUITKA_BYTECODE_FLAG },
    { (char *)"datetime", NULL, &constant_bin[ 943632 ], 55513, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm", NULL, &constant_bin[ 999145 ], 4477, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"dbm.dumb", NULL, &constant_bin[ 1003622 ], 8126, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm.gnu", NULL, &constant_bin[ 1011748 ], 255, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm.ndbm", NULL, &constant_bin[ 1012003 ], 254, NUITKA_BYTECODE_FLAG },
    { (char *)"decimal", NULL, &constant_bin[ 1012257 ], 171325, NUITKA_BYTECODE_FLAG },
    { (char *)"difflib", NULL, &constant_bin[ 1183582 ], 62310, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils", NULL, &constant_bin[ 1245892 ], 447, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"distutils.archive_util", NULL, &constant_bin[ 1246339 ], 6852, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.bcppcompiler", NULL, &constant_bin[ 1253191 ], 7286, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.ccompiler", NULL, &constant_bin[ 1260477 ], 34848, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.cmd", NULL, &constant_bin[ 1295325 ], 15676, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command", NULL, &constant_bin[ 1311001 ], 612, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"distutils.command.bdist", NULL, &constant_bin[ 1311613 ], 4089, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_dumb", NULL, &constant_bin[ 1315702 ], 4009, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_rpm", NULL, &constant_bin[ 1319711 ], 14257, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_wininst", NULL, &constant_bin[ 1333968 ], 9050, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build", NULL, &constant_bin[ 1343018 ], 4327, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_clib", NULL, &constant_bin[ 1347345 ], 5447, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_ext", NULL, &constant_bin[ 1352792 ], 18128, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_py", NULL, &constant_bin[ 1370920 ], 11501, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_scripts", NULL, &constant_bin[ 1382421 ], 4756, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.check", NULL, &constant_bin[ 1387177 ], 5282, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.clean", NULL, &constant_bin[ 1392459 ], 2408, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.config", NULL, &constant_bin[ 1394867 ], 11054, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install", NULL, &constant_bin[ 1405921 ], 15027, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_data", NULL, &constant_bin[ 1420948 ], 2585, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_egg_info", NULL, &constant_bin[ 1423533 ], 3231, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_headers", NULL, &constant_bin[ 1426764 ], 1892, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_lib", NULL, &constant_bin[ 1428656 ], 5686, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_scripts", NULL, &constant_bin[ 1434342 ], 2417, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.register", NULL, &constant_bin[ 1436759 ], 9223, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.sdist", NULL, &constant_bin[ 1445982 ], 14165, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.upload", NULL, &constant_bin[ 1460147 ], 5724, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.config", NULL, &constant_bin[ 1465871 ], 3842, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.core", NULL, &constant_bin[ 1469713 ], 7151, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.cygwinccompiler", NULL, &constant_bin[ 1476864 ], 9254, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.debug", NULL, &constant_bin[ 1486118 ], 252, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dep_util", NULL, &constant_bin[ 1486370 ], 2894, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dir_util", NULL, &constant_bin[ 1489264 ], 6236, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dist", NULL, &constant_bin[ 1495500 ], 36740, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.errors", NULL, &constant_bin[ 1532240 ], 5758, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.extension", NULL, &constant_bin[ 1537998 ], 7445, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.fancy_getopt", NULL, &constant_bin[ 1545443 ], 11532, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.file_util", NULL, &constant_bin[ 1556975 ], 6337, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.filelist", NULL, &constant_bin[ 1563312 ], 10149, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.log", NULL, &constant_bin[ 1573461 ], 2519, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.msvccompiler", NULL, &constant_bin[ 1575980 ], 15982, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.spawn", NULL, &constant_bin[ 1591962 ], 5408, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.sysconfig", NULL, &constant_bin[ 1597370 ], 13135, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests", NULL, &constant_bin[ 1610505 ], 1383, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"distutils.tests.support", NULL, &constant_bin[ 1611888 ], 8028, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_archive_util", NULL, &constant_bin[ 1619916 ], 13053, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_bdist", NULL, &constant_bin[ 1632969 ], 1798, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_bdist_dumb", NULL, &constant_bin[ 1634767 ], 3295, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_bdist_msi", NULL, &constant_bin[ 1638062 ], 1196, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_bdist_rpm", NULL, &constant_bin[ 1639258 ], 4447, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_bdist_wininst", NULL, &constant_bin[ 1643705 ], 1205, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_build", NULL, &constant_bin[ 1644910 ], 1830, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_build_clib", NULL, &constant_bin[ 1646740 ], 4393, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_build_ext", NULL, &constant_bin[ 1651133 ], 13522, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_build_py", NULL, &constant_bin[ 1664655 ], 5597, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_build_scripts", NULL, &constant_bin[ 1670252 ], 3768, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_check", NULL, &constant_bin[ 1674020 ], 4096, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_clean", NULL, &constant_bin[ 1678116 ], 1833, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_cmd", NULL, &constant_bin[ 1679949 ], 4662, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_config", NULL, &constant_bin[ 1684611 ], 3840, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_config_cmd", NULL, &constant_bin[ 1688451 ], 3407, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_core", NULL, &constant_bin[ 1691858 ], 3540, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_cygwinccompiler", NULL, &constant_bin[ 1695398 ], 4995, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_dep_util", NULL, &constant_bin[ 1700393 ], 2615, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_dir_util", NULL, &constant_bin[ 1703008 ], 5305, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_dist", NULL, &constant_bin[ 1708313 ], 15593, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_extension", NULL, &constant_bin[ 1723906 ], 2788, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_file_util", NULL, &constant_bin[ 1726694 ], 4647, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_filelist", NULL, &constant_bin[ 1731341 ], 7757, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_install", NULL, &constant_bin[ 1739098 ], 7692, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_install_data", NULL, &constant_bin[ 1746790 ], 2325, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_install_headers", NULL, &constant_bin[ 1749115 ], 1572, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_install_lib", NULL, &constant_bin[ 1750687 ], 3863, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_install_scripts", NULL, &constant_bin[ 1754550 ], 2691, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_log", NULL, &constant_bin[ 1757241 ], 1422, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_msvc9compiler", NULL, &constant_bin[ 1758663 ], 5937, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_msvccompiler", NULL, &constant_bin[ 1764600 ], 3213, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_register", NULL, &constant_bin[ 1767813 ], 8366, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_sdist", NULL, &constant_bin[ 1776179 ], 13631, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_spawn", NULL, &constant_bin[ 1789810 ], 2030, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_sysconfig", NULL, &constant_bin[ 1791840 ], 8044, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_text_file", NULL, &constant_bin[ 1799884 ], 2554, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_unixccompiler", NULL, &constant_bin[ 1802438 ], 5063, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_upload", NULL, &constant_bin[ 1807501 ], 5041, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_util", NULL, &constant_bin[ 1812542 ], 9516, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_version", NULL, &constant_bin[ 1822058 ], 2716, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.tests.test_versionpredicate", NULL, &constant_bin[ 1824774 ], 598, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.text_file", NULL, &constant_bin[ 1825372 ], 8933, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.unixccompiler", NULL, &constant_bin[ 1834305 ], 7235, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.util", NULL, &constant_bin[ 1841540 ], 16568, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.version", NULL, &constant_bin[ 1858108 ], 7814, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.versionpredicate", NULL, &constant_bin[ 1865922 ], 5410, NUITKA_BYTECODE_FLAG },
    { (char *)"doctest", NULL, &constant_bin[ 1871332 ], 79779, NUITKA_BYTECODE_FLAG },
    { (char *)"dummy_threading", NULL, &constant_bin[ 1951111 ], 1240, NUITKA_BYTECODE_FLAG },
    { (char *)"email", NULL, &constant_bin[ 1952351 ], 1802, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"email._encoded_words", NULL, &constant_bin[ 1954153 ], 6087, NUITKA_BYTECODE_FLAG },
    { (char *)"email._header_value_parser", NULL, &constant_bin[ 1960240 ], 87305, NUITKA_BYTECODE_FLAG },
    { (char *)"email._parseaddr", NULL, &constant_bin[ 2047545 ], 13779, NUITKA_BYTECODE_FLAG },
    { (char *)"email._policybase", NULL, &constant_bin[ 2061324 ], 15190, NUITKA_BYTECODE_FLAG },
    { (char *)"email.base64mime", NULL, &constant_bin[ 2076514 ], 3410, NUITKA_BYTECODE_FLAG },
    { (char *)"email.charset", NULL, &constant_bin[ 2079924 ], 12097, NUITKA_BYTECODE_FLAG },
    { (char *)"email.contentmanager", NULL, &constant_bin[ 2092021 ], 8148, NUITKA_BYTECODE_FLAG },
    { (char *)"email.encoders", NULL, &constant_bin[ 2100169 ], 1785, NUITKA_BYTECODE_FLAG },
    { (char *)"email.errors", NULL, &constant_bin[ 2101954 ], 6316, NUITKA_BYTECODE_FLAG },
    { (char *)"email.feedparser", NULL, &constant_bin[ 2108270 ], 11791, NUITKA_BYTECODE_FLAG },
    { (char *)"email.generator", NULL, &constant_bin[ 2120061 ], 13638, NUITKA_BYTECODE_FLAG },
    { (char *)"email.header", NULL, &constant_bin[ 2133699 ], 17724, NUITKA_BYTECODE_FLAG },
    { (char *)"email.headerregistry", NULL, &constant_bin[ 2151423 ], 22658, NUITKA_BYTECODE_FLAG },
    { (char *)"email.iterators", NULL, &constant_bin[ 2174081 ], 2069, NUITKA_BYTECODE_FLAG },
    { (char *)"email.message", NULL, &constant_bin[ 2176150 ], 39306, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime", NULL, &constant_bin[ 2215456 ], 180, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"email.mime.application", NULL, &constant_bin[ 2215636 ], 1502, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.audio", NULL, &constant_bin[ 2217138 ], 2719, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.base", NULL, &constant_bin[ 2219857 ], 1059, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.image", NULL, &constant_bin[ 2220916 ], 1961, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.message", NULL, &constant_bin[ 2222877 ], 1379, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.multipart", NULL, &constant_bin[ 2224256 ], 1594, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.nonmultipart", NULL, &constant_bin[ 2225850 ], 836, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.text", NULL, &constant_bin[ 2226686 ], 1404, NUITKA_BYTECODE_FLAG },
    { (char *)"email.parser", NULL, &constant_bin[ 2228090 ], 5953, NUITKA_BYTECODE_FLAG },
    { (char *)"email.policy", NULL, &constant_bin[ 2234043 ], 9808, NUITKA_BYTECODE_FLAG },
    { (char *)"email.quoprimime", NULL, &constant_bin[ 2243851 ], 8150, NUITKA_BYTECODE_FLAG },
    { (char *)"email.utils", NULL, &constant_bin[ 2252001 ], 10499, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.base64_codec", NULL, &constant_bin[ 2262500 ], 2610, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.big5", NULL, &constant_bin[ 2265110 ], 1608, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.big5hkscs", NULL, &constant_bin[ 2266718 ], 1618, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.bz2_codec", NULL, &constant_bin[ 2268336 ], 3520, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.charmap", NULL, &constant_bin[ 2271856 ], 3132, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp037", NULL, &constant_bin[ 2274988 ], 2587, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1006", NULL, &constant_bin[ 2277575 ], 2663, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1026", NULL, &constant_bin[ 2280238 ], 2591, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1125", NULL, &constant_bin[ 2282829 ], 7608, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1140", NULL, &constant_bin[ 2290437 ], 2577, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1250", NULL, &constant_bin[ 2293014 ], 2614, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1251", NULL, &constant_bin[ 2295628 ], 2611, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1252", NULL, &constant_bin[ 2298239 ], 2614, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1253", NULL, &constant_bin[ 2300853 ], 2627, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1254", NULL, &constant_bin[ 2303480 ], 2616, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1255", NULL, &constant_bin[ 2306096 ], 2635, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1256", NULL, &constant_bin[ 2308731 ], 2613, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1257", NULL, &constant_bin[ 2311344 ], 2621, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp1258", NULL, &constant_bin[ 2313965 ], 2619, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp273", NULL, &constant_bin[ 2316584 ], 2573, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp424", NULL, &constant_bin[ 2319157 ], 2617, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp500", NULL, &constant_bin[ 2321774 ], 2587, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp720", NULL, &constant_bin[ 2324361 ], 2684, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp737", NULL, &constant_bin[ 2327045 ], 7653, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp775", NULL, &constant_bin[ 2334698 ], 7439, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp850", NULL, &constant_bin[ 2342137 ], 7172, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp852", NULL, &constant_bin[ 2349309 ], 7441, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp855", NULL, &constant_bin[ 2356750 ], 7622, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp856", NULL, &constant_bin[ 2364372 ], 2649, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp857", NULL, &constant_bin[ 2367021 ], 7157, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp858", NULL, &constant_bin[ 2374178 ], 7142, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp860", NULL, &constant_bin[ 2381320 ], 7408, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp861", NULL, &constant_bin[ 2388728 ], 7419, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp862", NULL, &constant_bin[ 2396147 ], 7554, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp863", NULL, &constant_bin[ 2403701 ], 7419, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp864", NULL, &constant_bin[ 2411120 ], 7549, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp865", NULL, &constant_bin[ 2418669 ], 7419, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp866", NULL, &constant_bin[ 2426088 ], 7654, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp869", NULL, &constant_bin[ 2433742 ], 7466, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp874", NULL, &constant_bin[ 2441208 ], 2715, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp875", NULL, &constant_bin[ 2443923 ], 2584, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp932", NULL, &constant_bin[ 2446507 ], 1610, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp949", NULL, &constant_bin[ 2448117 ], 1610, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.cp950", NULL, &constant_bin[ 2449727 ], 1610, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.euc_jis_2004", NULL, &constant_bin[ 2451337 ], 1624, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.euc_jisx0213", NULL, &constant_bin[ 2452961 ], 1624, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.euc_jp", NULL, &constant_bin[ 2454585 ], 1612, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.euc_kr", NULL, &constant_bin[ 2456197 ], 1612, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.gb18030", NULL, &constant_bin[ 2457809 ], 1614, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.gb2312", NULL, &constant_bin[ 2459423 ], 1612, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.gbk", NULL, &constant_bin[ 2461035 ], 1606, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.hex_codec", NULL, &constant_bin[ 2462641 ], 2597, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.hp_roman8", NULL, &constant_bin[ 2465238 ], 2760, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.hz", NULL, &constant_bin[ 2467998 ], 1604, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp", NULL, &constant_bin[ 2469602 ], 1625, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp_1", NULL, &constant_bin[ 2471227 ], 1629, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp_2", NULL, &constant_bin[ 2472856 ], 1629, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp_2004", NULL, &constant_bin[ 2474485 ], 1635, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp_3", NULL, &constant_bin[ 2476120 ], 1629, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_jp_ext", NULL, &constant_bin[ 2477749 ], 1633, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso2022_kr", NULL, &constant_bin[ 2479382 ], 1625, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_1", NULL, &constant_bin[ 2481007 ], 2586, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_10", NULL, &constant_bin[ 2483593 ], 2591, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_11", NULL, &constant_bin[ 2486184 ], 2685, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_13", NULL, &constant_bin[ 2488869 ], 2594, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_14", NULL, &constant_bin[ 2491463 ], 2612, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_15", NULL, &constant_bin[ 2494075 ], 2591, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_16", NULL, &constant_bin[ 2496666 ], 2593, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_2", NULL, &constant_bin[ 2499259 ], 2586, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_3", NULL, &constant_bin[ 2501845 ], 2593, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_4", NULL, &constant_bin[ 2504438 ], 2586, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_5", NULL, &constant_bin[ 2507024 ], 2587, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_6", NULL, &constant_bin[ 2509611 ], 2631, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_7", NULL, &constant_bin[ 2512242 ], 2594, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_8", NULL, &constant_bin[ 2514836 ], 2625, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.iso8859_9", NULL, &constant_bin[ 2517461 ], 2586, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.johab", NULL, &constant_bin[ 2520047 ], 1610, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.koi8_r", NULL, &constant_bin[ 2521657 ], 2638, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.koi8_t", NULL, &constant_bin[ 2524295 ], 2549, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.koi8_u", NULL, &constant_bin[ 2526844 ], 2624, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.kz1048", NULL, &constant_bin[ 2529468 ], 2601, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_arabic", NULL, &constant_bin[ 2532069 ], 7325, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_centeuro", NULL, &constant_bin[ 2539394 ], 2625, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_croatian", NULL, &constant_bin[ 2542019 ], 2633, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_cyrillic", NULL, &constant_bin[ 2544652 ], 2623, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_farsi", NULL, &constant_bin[ 2547275 ], 2567, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_greek", NULL, &constant_bin[ 2549842 ], 2607, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_iceland", NULL, &constant_bin[ 2552449 ], 2626, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_latin2", NULL, &constant_bin[ 2555075 ], 2767, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_roman", NULL, &constant_bin[ 2557842 ], 2624, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_romanian", NULL, &constant_bin[ 2560466 ], 2634, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.mac_turkish", NULL, &constant_bin[ 2563100 ], 2627, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.palmos", NULL, &constant_bin[ 2565727 ], 2614, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.ptcp154", NULL, &constant_bin[ 2568341 ], 2708, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.punycode", NULL, &constant_bin[ 2571049 ], 7135, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.quopri_codec", NULL, &constant_bin[ 2578184 ], 2642, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.raw_unicode_escape", NULL, &constant_bin[ 2580826 ], 1918, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.rot_13", NULL, &constant_bin[ 2582744 ], 3134, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.shift_jis", NULL, &constant_bin[ 2585878 ], 1618, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.shift_jis_2004", NULL, &constant_bin[ 2587496 ], 1628, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.shift_jisx0213", NULL, &constant_bin[ 2589124 ], 1628, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.tis_620", NULL, &constant_bin[ 2590752 ], 2676, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.undefined", NULL, &constant_bin[ 2593428 ], 2310, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.unicode_escape", NULL, &constant_bin[ 2595738 ], 1898, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.unicode_internal", NULL, &constant_bin[ 2597636 ], 1908, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_16", NULL, &constant_bin[ 2599544 ], 5282, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_16_be", NULL, &constant_bin[ 2604826 ], 1770, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_16_le", NULL, &constant_bin[ 2606596 ], 1770, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_32", NULL, &constant_bin[ 2608366 ], 5175, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_32_be", NULL, &constant_bin[ 2613541 ], 1663, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_32_le", NULL, &constant_bin[ 2615204 ], 1663, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_7", NULL, &constant_bin[ 2616867 ], 1691, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.utf_8_sig", NULL, &constant_bin[ 2618558 ], 4882, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.uu_codec", NULL, &constant_bin[ 2623440 ], 3501, NUITKA_BYTECODE_FLAG },
    { (char *)"encodings.zlib_codec", NULL, &constant_bin[ 2626941 ], 3362, NUITKA_BYTECODE_FLAG },
    { (char *)"filecmp", NULL, &constant_bin[ 2630303 ], 9127, NUITKA_BYTECODE_FLAG },
    { (char *)"fileinput", NULL, &constant_bin[ 2639430 ], 14244, NUITKA_BYTECODE_FLAG },
    { (char *)"fnmatch", NULL, &constant_bin[ 2653674 ], 3172, NUITKA_BYTECODE_FLAG },
    { (char *)"formatter", NULL, &constant_bin[ 2656846 ], 18852, NUITKA_BYTECODE_FLAG },
    { (char *)"fractions", NULL, &constant_bin[ 2675698 ], 20052, NUITKA_BYTECODE_FLAG },
    { (char *)"ftplib", NULL, &constant_bin[ 2695750 ], 30132, NUITKA_BYTECODE_FLAG },
    { (char *)"getopt", NULL, &constant_bin[ 2725882 ], 6741, NUITKA_BYTECODE_FLAG },
    { (char *)"getpass", NULL, &constant_bin[ 2732623 ], 4600, NUITKA_BYTECODE_FLAG },
    { (char *)"gettext", NULL, &constant_bin[ 2737223 ], 13089, NUITKA_BYTECODE_FLAG },
    { (char *)"glob", NULL, &constant_bin[ 2750312 ], 4243, NUITKA_BYTECODE_FLAG },
    { (char *)"gzip", NULL, &constant_bin[ 2754555 ], 17682, NUITKA_BYTECODE_FLAG },
    { (char *)"hashlib", NULL, &constant_bin[ 2772237 ], 6399, NUITKA_BYTECODE_FLAG },
    { (char *)"hmac", NULL, &constant_bin[ 2778636 ], 5172, NUITKA_BYTECODE_FLAG },
    { (char *)"html", NULL, &constant_bin[ 2783808 ], 3673, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"html.entities", NULL, &constant_bin[ 2787481 ], 55481, NUITKA_BYTECODE_FLAG },
    { (char *)"html.parser", NULL, &constant_bin[ 2842962 ], 12273, NUITKA_BYTECODE_FLAG },
    { (char *)"http", NULL, &constant_bin[ 2855235 ], 6775, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"http.client", NULL, &constant_bin[ 2862010 ], 33003, NUITKA_BYTECODE_FLAG },
    { (char *)"http.cookiejar", NULL, &constant_bin[ 2895013 ], 58343, NUITKA_BYTECODE_FLAG },
    { (char *)"http.cookies", NULL, &constant_bin[ 2953356 ], 17252, NUITKA_BYTECODE_FLAG },
    { (char *)"http.server", NULL, &constant_bin[ 2970608 ], 34459, NUITKA_BYTECODE_FLAG },
    { (char *)"imaplib", NULL, &constant_bin[ 3005067 ], 44758, NUITKA_BYTECODE_FLAG },
    { (char *)"imghdr", NULL, &constant_bin[ 3049825 ], 4539, NUITKA_BYTECODE_FLAG },
    { (char *)"imp", NULL, &constant_bin[ 3054364 ], 10496, NUITKA_BYTECODE_FLAG },
    { (char *)"importlib.abc", NULL, &constant_bin[ 3064860 ], 11795, NUITKA_BYTECODE_FLAG },
    { (char *)"importlib.util", NULL, &constant_bin[ 3076655 ], 9807, NUITKA_BYTECODE_FLAG },
    { (char *)"ipaddress", NULL, &constant_bin[ 3086462 ], 66336, NUITKA_BYTECODE_FLAG },
    { (char *)"json", NULL, &constant_bin[ 3152798 ], 12295, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"json.decoder", NULL, &constant_bin[ 3165093 ], 10715, NUITKA_BYTECODE_FLAG },
    { (char *)"json.encoder", NULL, &constant_bin[ 3175808 ], 12043, NUITKA_BYTECODE_FLAG },
    { (char *)"json.scanner", NULL, &constant_bin[ 3187851 ], 2253, NUITKA_BYTECODE_FLAG },
    { (char *)"json.tool", NULL, &constant_bin[ 3190104 ], 1723, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3", NULL, &constant_bin[ 3191827 ], 177, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.btm_matcher", NULL, &constant_bin[ 3192004 ], 5357, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.btm_utils", NULL, &constant_bin[ 3197361 ], 6827, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixer_base", NULL, &constant_bin[ 3204188 ], 6568, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixer_util", NULL, &constant_bin[ 3210756 ], 13393, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes", NULL, &constant_bin[ 3224149 ], 183, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.fixes.fix_apply", NULL, &constant_bin[ 3224332 ], 1726, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_asserts", NULL, &constant_bin[ 3226058 ], 1403, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_basestring", NULL, &constant_bin[ 3227461 ], 728, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_buffer", NULL, &constant_bin[ 3228189 ], 880, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_callable", NULL, &constant_bin[ 3229069 ], 1385, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_dict", NULL, &constant_bin[ 3230454 ], 3709, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_except", NULL, &constant_bin[ 3234163 ], 3080, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_exec", NULL, &constant_bin[ 3237243 ], 1305, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_execfile", NULL, &constant_bin[ 3238548 ], 1885, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_exitfunc", NULL, &constant_bin[ 3240433 ], 2500, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_filter", NULL, &constant_bin[ 3242933 ], 2135, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_funcattrs", NULL, &constant_bin[ 3245068 ], 1047, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_future", NULL, &constant_bin[ 3246115 ], 855, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_getcwdu", NULL, &constant_bin[ 3246970 ], 858, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_has_key", NULL, &constant_bin[ 3247828 ], 3207, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_idioms", NULL, &constant_bin[ 3251035 ], 4187, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_import", NULL, &constant_bin[ 3255222 ], 3053, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_imports", NULL, &constant_bin[ 3258275 ], 4763, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_imports2", NULL, &constant_bin[ 3263038 ], 608, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_input", NULL, &constant_bin[ 3263646 ], 1044, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_intern", NULL, &constant_bin[ 3264690 ], 1090, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_isinstance", NULL, &constant_bin[ 3265780 ], 1715, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_itertools", NULL, &constant_bin[ 3267495 ], 1679, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_itertools_imports", NULL, &constant_bin[ 3269174 ], 1825, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_long", NULL, &constant_bin[ 3270999 ], 776, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_map", NULL, &constant_bin[ 3271775 ], 2881, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_metaclass", NULL, &constant_bin[ 3274656 ], 5987, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_methodattrs", NULL, &constant_bin[ 3280643 ], 1019, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_ne", NULL, &constant_bin[ 3281662 ], 887, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_next", NULL, &constant_bin[ 3282549 ], 3342, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_nonzero", NULL, &constant_bin[ 3285891 ], 1012, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_numliterals", NULL, &constant_bin[ 3286903 ], 1143, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_operator", NULL, &constant_bin[ 3288046 ], 4526, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_paren", NULL, &constant_bin[ 3292572 ], 1474, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_print", NULL, &constant_bin[ 3294046 ], 2622, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_raise", NULL, &constant_bin[ 3296668 ], 2477, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_raw_input", NULL, &constant_bin[ 3299145 ], 865, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_reduce", NULL, &constant_bin[ 3300010 ], 1198, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_reload", NULL, &constant_bin[ 3301208 ], 1090, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_renames", NULL, &constant_bin[ 3302298 ], 2152, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_repr", NULL, &constant_bin[ 3304450 ], 933, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_set_literal", NULL, &constant_bin[ 3305383 ], 1841, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_standarderror", NULL, &constant_bin[ 3307224 ], 785, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_sys_exc", NULL, &constant_bin[ 3308009 ], 1531, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_throw", NULL, &constant_bin[ 3309540 ], 1981, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_tuple_params", NULL, &constant_bin[ 3311521 ], 5092, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_types", NULL, &constant_bin[ 3316613 ], 2029, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_unicode", NULL, &constant_bin[ 3318642 ], 1689, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_urllib", NULL, &constant_bin[ 3320331 ], 6551, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_ws_comma", NULL, &constant_bin[ 3326882 ], 1251, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_xrange", NULL, &constant_bin[ 3328133 ], 2754, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_xreadlines", NULL, &constant_bin[ 3330887 ], 1207, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_zip", NULL, &constant_bin[ 3332094 ], 1261, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.main", NULL, &constant_bin[ 3333355 ], 9189, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.patcomp", NULL, &constant_bin[ 3342544 ], 6373, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2", NULL, &constant_bin[ 3348917 ], 215, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.pgen2.driver", NULL, &constant_bin[ 3349132 ], 4681, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.grammar", NULL, &constant_bin[ 3353813 ], 5742, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.literals", NULL, &constant_bin[ 3359555 ], 1786, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.parse", NULL, &constant_bin[ 3361341 ], 6751, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.pgen", NULL, &constant_bin[ 3368092 ], 11052, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.token", NULL, &constant_bin[ 3379144 ], 2066, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.tokenize", NULL, &constant_bin[ 3381210 ], 16000, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pygram", NULL, &constant_bin[ 3397210 ], 1300, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pytree", NULL, &constant_bin[ 3398510 ], 26910, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.refactor", NULL, &constant_bin[ 3425420 ], 22845, NUITKA_BYTECODE_FLAG },
    { (char *)"logging", NULL, &constant_bin[ 3448265 ], 61440, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"logging.config", NULL, &constant_bin[ 3509705 ], 25454, NUITKA_BYTECODE_FLAG },
    { (char *)"logging.handlers", NULL, &constant_bin[ 3535159 ], 45077, NUITKA_BYTECODE_FLAG },
    { (char *)"lzma", NULL, &constant_bin[ 3580236 ], 12516, NUITKA_BYTECODE_FLAG },
    { (char *)"macpath", NULL, &constant_bin[ 3592752 ], 6184, NUITKA_BYTECODE_FLAG },
    { (char *)"macurl2path", NULL, &constant_bin[ 3598936 ], 2125, NUITKA_BYTECODE_FLAG },
    { (char *)"mailbox", NULL, &constant_bin[ 3601061 ], 69839, NUITKA_BYTECODE_FLAG },
    { (char *)"mailcap", NULL, &constant_bin[ 3670900 ], 6546, NUITKA_BYTECODE_FLAG },
    { (char *)"mimetypes", NULL, &constant_bin[ 3677446 ], 16637, NUITKA_BYTECODE_FLAG },
    { (char *)"modulefinder", NULL, &constant_bin[ 3694083 ], 17279, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing", NULL, &constant_bin[ 3711362 ], 604, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"multiprocessing.connection", NULL, &constant_bin[ 3711966 ], 27254, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.context", NULL, &constant_bin[ 3739220 ], 13553, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.dummy", NULL, &constant_bin[ 3752773 ], 4088, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"multiprocessing.dummy.connection", NULL, &constant_bin[ 3756861 ], 2708, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.forkserver", NULL, &constant_bin[ 3759569 ], 7121, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.heap", NULL, &constant_bin[ 3766690 ], 6808, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.managers", NULL, &constant_bin[ 3773498 ], 35553, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.pool", NULL, &constant_bin[ 3809051 ], 22892, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_fork", NULL, &constant_bin[ 3831943 ], 2422, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_forkserver", NULL, &constant_bin[ 3834365 ], 2585, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_spawn_posix", NULL, &constant_bin[ 3836950 ], 2356, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.process", NULL, &constant_bin[ 3839306 ], 8940, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.queues", NULL, &constant_bin[ 3848246 ], 9919, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.reduction", NULL, &constant_bin[ 3858165 ], 7806, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.resource_sharer", NULL, &constant_bin[ 3865971 ], 5675, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.semaphore_tracker", NULL, &constant_bin[ 3871646 ], 3763, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.sharedctypes", NULL, &constant_bin[ 3875409 ], 7529, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.spawn", NULL, &constant_bin[ 3882938 ], 7078, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.synchronize", NULL, &constant_bin[ 3890016 ], 12346, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.util", NULL, &constant_bin[ 3902362 ], 9987, NUITKA_BYTECODE_FLAG },
    { (char *)"netrc", NULL, &constant_bin[ 3912349 ], 4295, NUITKA_BYTECODE_FLAG },
    { (char *)"nntplib", NULL, &constant_bin[ 3916644 ], 36122, NUITKA_BYTECODE_FLAG },
    { (char *)"ntpath", NULL, &constant_bin[ 3952766 ], 14856, NUITKA_BYTECODE_FLAG },
    { (char *)"nturl2path", NULL, &constant_bin[ 3967622 ], 1736, NUITKA_BYTECODE_FLAG },
    { (char *)"numbers", NULL, &constant_bin[ 3969358 ], 12708, NUITKA_BYTECODE_FLAG },
    { (char *)"optparse", NULL, &constant_bin[ 3982066 ], 51369, NUITKA_BYTECODE_FLAG },
    { (char *)"pathlib", NULL, &constant_bin[ 4033435 ], 43631, NUITKA_BYTECODE_FLAG },
    { (char *)"pdb", NULL, &constant_bin[ 4077066 ], 49379, NUITKA_BYTECODE_FLAG },
    { (char *)"pickletools", NULL, &constant_bin[ 4126445 ], 70159, NUITKA_BYTECODE_FLAG },
    { (char *)"pipes", NULL, &constant_bin[ 4196604 ], 8397, NUITKA_BYTECODE_FLAG },
    { (char *)"pkgutil", NULL, &constant_bin[ 4205001 ], 17519, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-darwin.IN", NULL, &constant_bin[ 4222520 ], 19232, NUITKA_BYTECODE_FLAG },
    { (char *)"platform", NULL, &constant_bin[ 4241752 ], 31712, NUITKA_BYTECODE_FLAG },
    { (char *)"plistlib", NULL, &constant_bin[ 4273464 ], 29876, NUITKA_BYTECODE_FLAG },
    { (char *)"poplib", NULL, &constant_bin[ 4303340 ], 13969, NUITKA_BYTECODE_FLAG },
    { (char *)"pprint", NULL, &constant_bin[ 4317309 ], 17521, NUITKA_BYTECODE_FLAG },
    { (char *)"profile", NULL, &constant_bin[ 4334830 ], 15126, NUITKA_BYTECODE_FLAG },
    { (char *)"pstats", NULL, &constant_bin[ 4349956 ], 23608, NUITKA_BYTECODE_FLAG },
    { (char *)"pty", NULL, &constant_bin[ 4373564 ], 4245, NUITKA_BYTECODE_FLAG },
    { (char *)"py_compile", NULL, &constant_bin[ 4377809 ], 6919, NUITKA_BYTECODE_FLAG },
    { (char *)"pyclbr", NULL, &constant_bin[ 4384728 ], 9149, NUITKA_BYTECODE_FLAG },
    { (char *)"pydoc", NULL, &constant_bin[ 4393877 ], 90540, NUITKA_BYTECODE_FLAG },
    { (char *)"pydoc_data", NULL, &constant_bin[ 4484417 ], 180, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"pydoc_data.topics", NULL, &constant_bin[ 4484597 ], 385791, NUITKA_BYTECODE_FLAG },
    { (char *)"queue", NULL, &constant_bin[ 4870388 ], 9235, NUITKA_BYTECODE_FLAG },
    { (char *)"quopri", NULL, &constant_bin[ 4879623 ], 6442, NUITKA_BYTECODE_FLAG },
    { (char *)"random", NULL, &constant_bin[ 4886065 ], 19026, NUITKA_BYTECODE_FLAG },
    { (char *)"rlcompleter", NULL, &constant_bin[ 4905091 ], 5654, NUITKA_BYTECODE_FLAG },
    { (char *)"runpy", NULL, &constant_bin[ 4910745 ], 7752, NUITKA_BYTECODE_FLAG },
    { (char *)"sched", NULL, &constant_bin[ 4918497 ], 6407, NUITKA_BYTECODE_FLAG },
    { (char *)"selectors", NULL, &constant_bin[ 4924904 ], 18337, NUITKA_BYTECODE_FLAG },
    { (char *)"shelve", NULL, &constant_bin[ 4943241 ], 9981, NUITKA_BYTECODE_FLAG },
    { (char *)"shlex", NULL, &constant_bin[ 4953222 ], 7379, NUITKA_BYTECODE_FLAG },
    { (char *)"shutil", NULL, &constant_bin[ 4960601 ], 32769, NUITKA_BYTECODE_FLAG },
    { (char *)"signal", NULL, &constant_bin[ 4993370 ], 2818, NUITKA_BYTECODE_FLAG },
    { (char *)"site", NULL, &constant_bin[ 4996188 ], 14818, NUITKA_BYTECODE_FLAG },
    { (char *)"smtpd", NULL, &constant_bin[ 5011006 ], 29349, NUITKA_BYTECODE_FLAG },
    { (char *)"smtplib", NULL, &constant_bin[ 5040355 ], 37047, NUITKA_BYTECODE_FLAG },
    { (char *)"sndhdr", NULL, &constant_bin[ 5077402 ], 6946, NUITKA_BYTECODE_FLAG },
    { (char *)"socket", NULL, &constant_bin[ 5084348 ], 23145, NUITKA_BYTECODE_FLAG },
    { (char *)"socketserver", NULL, &constant_bin[ 5107493 ], 23222, NUITKA_BYTECODE_FLAG },
    { (char *)"sqlite3", NULL, &constant_bin[ 5130715 ], 210, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"sqlite3.dbapi2", NULL, &constant_bin[ 5130925 ], 2745, NUITKA_BYTECODE_FLAG },
    { (char *)"sqlite3.dump", NULL, &constant_bin[ 5133670 ], 2086, NUITKA_BYTECODE_FLAG },
    { (char *)"ssl", NULL, &constant_bin[ 5135756 ], 35667, NUITKA_BYTECODE_FLAG },
    { (char *)"statistics", NULL, &constant_bin[ 5171423 ], 16012, NUITKA_BYTECODE_FLAG },
    { (char *)"string", NULL, &constant_bin[ 5187435 ], 8538, NUITKA_BYTECODE_FLAG },
    { (char *)"subprocess", NULL, &constant_bin[ 5195973 ], 46639, NUITKA_BYTECODE_FLAG },
    { (char *)"sunau", NULL, &constant_bin[ 5242612 ], 18242, NUITKA_BYTECODE_FLAG },
    { (char *)"symbol", NULL, &constant_bin[ 5260854 ], 2771, NUITKA_BYTECODE_FLAG },
    { (char *)"symtable", NULL, &constant_bin[ 5263625 ], 11058, NUITKA_BYTECODE_FLAG },
    { (char *)"sysconfig", NULL, &constant_bin[ 5274683 ], 16834, NUITKA_BYTECODE_FLAG },
    { (char *)"tabnanny", NULL, &constant_bin[ 5291517 ], 7742, NUITKA_BYTECODE_FLAG },
    { (char *)"tarfile", NULL, &constant_bin[ 5299259 ], 68828, NUITKA_BYTECODE_FLAG },
    { (char *)"telnetlib", NULL, &constant_bin[ 5368087 ], 19272, NUITKA_BYTECODE_FLAG },
    { (char *)"tempfile", NULL, &constant_bin[ 5387359 ], 23644, NUITKA_BYTECODE_FLAG },
    { (char *)"test", NULL, &constant_bin[ 5411003 ], 174, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"test.support", NULL, &constant_bin[ 5411177 ], 70013, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"textwrap", NULL, &constant_bin[ 5481190 ], 14246, NUITKA_BYTECODE_FLAG },
    { (char *)"this", NULL, &constant_bin[ 5495436 ], 1357, NUITKA_BYTECODE_FLAG },
    { (char *)"threading", NULL, &constant_bin[ 5496793 ], 38952, NUITKA_BYTECODE_FLAG },
    { (char *)"timeit", NULL, &constant_bin[ 5535745 ], 11051, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter", NULL, &constant_bin[ 5546796 ], 184052, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"tkinter.colorchooser", NULL, &constant_bin[ 5730848 ], 1248, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.commondialog", NULL, &constant_bin[ 5732096 ], 1320, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.constants", NULL, &constant_bin[ 5733416 ], 1848, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.dialog", NULL, &constant_bin[ 5735264 ], 1666, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.dnd", NULL, &constant_bin[ 5736930 ], 11871, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.filedialog", NULL, &constant_bin[ 5748801 ], 13471, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.font", NULL, &constant_bin[ 5762272 ], 6721, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.messagebox", NULL, &constant_bin[ 5768993 ], 3321, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.scrolledtext", NULL, &constant_bin[ 5772314 ], 2380, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.simpledialog", NULL, &constant_bin[ 5774694 ], 11435, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.tix", NULL, &constant_bin[ 5786129 ], 88927, NUITKA_BYTECODE_FLAG },
    { (char *)"tkinter.ttk", NULL, &constant_bin[ 5875056 ], 58279, NUITKA_BYTECODE_FLAG },
    { (char *)"trace", NULL, &constant_bin[ 5933335 ], 23980, NUITKA_BYTECODE_FLAG },
    { (char *)"traceback", NULL, &constant_bin[ 5957315 ], 20210, NUITKA_BYTECODE_FLAG },
    { (char *)"tracemalloc", NULL, &constant_bin[ 5977525 ], 17119, NUITKA_BYTECODE_FLAG },
    { (char *)"tty", NULL, &constant_bin[ 5994644 ], 1187, NUITKA_BYTECODE_FLAG },
    { (char *)"turtle", NULL, &constant_bin[ 5995831 ], 138901, NUITKA_BYTECODE_FLAG },
    { (char *)"typing", NULL, &constant_bin[ 6134732 ], 55202, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest", NULL, &constant_bin[ 6189934 ], 3131, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"unittest.case", NULL, &constant_bin[ 6193065 ], 50651, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.loader", NULL, &constant_bin[ 6243716 ], 15154, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.main", NULL, &constant_bin[ 6258870 ], 7719, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.mock", NULL, &constant_bin[ 6266589 ], 65585, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.result", NULL, &constant_bin[ 6332174 ], 7814, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.runner", NULL, &constant_bin[ 6339988 ], 7559, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.signals", NULL, &constant_bin[ 6347547 ], 2418, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.suite", NULL, &constant_bin[ 6349965 ], 9954, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.util", NULL, &constant_bin[ 6359919 ], 5268, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib", NULL, &constant_bin[ 6365187 ], 176, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"urllib.error", NULL, &constant_bin[ 6365363 ], 2964, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.parse", NULL, &constant_bin[ 6368327 ], 30139, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.request", NULL, &constant_bin[ 6398466 ], 75689, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.response", NULL, &constant_bin[ 6474155 ], 3436, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.robotparser", NULL, &constant_bin[ 6477591 ], 6754, NUITKA_BYTECODE_FLAG },
    { (char *)"uu", NULL, &constant_bin[ 6484345 ], 3996, NUITKA_BYTECODE_FLAG },
    { (char *)"uuid", NULL, &constant_bin[ 6488341 ], 21692, NUITKA_BYTECODE_FLAG },
    { (char *)"venv", NULL, &constant_bin[ 6510033 ], 16395, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"wave", NULL, &constant_bin[ 6526428 ], 19047, NUITKA_BYTECODE_FLAG },
    { (char *)"webbrowser", NULL, &constant_bin[ 6545475 ], 17074, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref", NULL, &constant_bin[ 6562549 ], 774, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"wsgiref.handlers", NULL, &constant_bin[ 6563323 ], 16961, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.headers", NULL, &constant_bin[ 6580284 ], 8194, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.simple_server", NULL, &constant_bin[ 6588478 ], 5690, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.util", NULL, &constant_bin[ 6594168 ], 5631, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.validate", NULL, &constant_bin[ 6599799 ], 15694, NUITKA_BYTECODE_FLAG },
    { (char *)"xdrlib", NULL, &constant_bin[ 6615493 ], 9007, NUITKA_BYTECODE_FLAG },
    { (char *)"xml", NULL, &constant_bin[ 6624500 ], 748, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.dom", NULL, &constant_bin[ 6625248 ], 5816, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.dom.NodeFilter", NULL, &constant_bin[ 6631064 ], 1056, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.domreg", NULL, &constant_bin[ 6632120 ], 2981, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.expatbuilder", NULL, &constant_bin[ 6635101 ], 29871, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.minicompat", NULL, &constant_bin[ 6664972 ], 3122, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.minidom", NULL, &constant_bin[ 6668094 ], 61423, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.pulldom", NULL, &constant_bin[ 6729517 ], 11622, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.xmlbuilder", NULL, &constant_bin[ 6741139 ], 14841, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree", NULL, &constant_bin[ 6755980 ], 179, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.etree.ElementInclude", NULL, &constant_bin[ 6756159 ], 1793, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.ElementPath", NULL, &constant_bin[ 6757952 ], 6756, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.ElementTree", NULL, &constant_bin[ 6764708 ], 47764, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.cElementTree", NULL, &constant_bin[ 6812472 ], 223, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.parsers", NULL, &constant_bin[ 6812695 ], 355, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.parsers.expat", NULL, &constant_bin[ 6813050 ], 396, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax", NULL, &constant_bin[ 6813446 ], 3391, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.sax._exceptions", NULL, &constant_bin[ 6816837 ], 5725, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.expatreader", NULL, &constant_bin[ 6822562 ], 13381, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.handler", NULL, &constant_bin[ 6835943 ], 12547, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.saxutils", NULL, &constant_bin[ 6848490 ], 13791, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.xmlreader", NULL, &constant_bin[ 6862281 ], 17571, NUITKA_BYTECODE_FLAG },
    { (char *)"xmlrpc", NULL, &constant_bin[ 6879852 ], 176, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xmlrpc.client", NULL, &constant_bin[ 6880028 ], 36778, NUITKA_BYTECODE_FLAG },
    { (char *)"xmlrpc.server", NULL, &constant_bin[ 6916806 ], 31230, NUITKA_BYTECODE_FLAG },
    { (char *)"zipapp", NULL, &constant_bin[ 6948036 ], 6057, NUITKA_BYTECODE_FLAG },
    { (char *)"zipfile", NULL, &constant_bin[ 6954093 ], 50004, NUITKA_BYTECODE_FLAG },
    { NULL, NULL, 0 }
};

void setupMetaPathBasedLoader( void )
{
    static bool init_done = false;

    if ( init_done == false )
    {
        registerMetaPathBasedUnfreezer( meta_path_loader_entries );
        init_done = true;
    }
}
#else

void setupMetaPathBasedLoader( void )
{
}

#endif
