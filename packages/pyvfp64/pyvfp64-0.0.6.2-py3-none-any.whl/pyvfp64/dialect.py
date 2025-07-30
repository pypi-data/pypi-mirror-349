import sys
from typing import TypeVar

from sqlalchemy.dialects import registry
from sqlalchemy.ext.compiler import compiles



import sqlalchemy
from sqlalchemy import (
    String,
    INTEGER,
    Integer,
    Float,
    DateTime,
    TypeDecorator,
    TEXT,
    NUMERIC,
    BIGINT,
    SMALLINT,
    VARCHAR,
    CHAR, FunctionElement, create_engine, pool,
)
from sqlalchemy.engine import default
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import compiler, elements, sqltypes

from types import SimpleNamespace
from pyvfp64.connection import connect as _vfp_connect, VFPConnection  # the adapter we built earlier
from pyvfp64.utils import convert_query_for_vfp
from pyvfp64.v_types import CustomDecimal, CustomInterval, CustomInteger, TrimmedString

dbapi_stub = SimpleNamespace(
    connect=_vfp_connect,
    paramstyle="qmark",      # any valid value is OK – we do our own
    apilevel="2.0",
    threadsafety=3,
)

dbapi_stub.Error         = Exception
dbapi_stub.DatabaseError = Exception
dbapi_stub.InterfaceError= Exception

class pow(FunctionElement):
    name = 'pow'


@compiles(pow)
def compile_pow(element, compiler, **kw):
    args = list(element.clauses)
    if len(args) != 2:
        raise Exception("pow() takes exactly two arguments.")

    base = compiler.process(args[0])
    exponent = compiler.process(args[1])

    # Replace with your custom logic here
    if base == '10' or base == '5':
        return f"{base} ^ {exponent}"
    else:
        return f"pow({base}, {exponent})"


ischema_names = {
    "N": sqltypes.Integer,
    "F": sqltypes.Float,
    "L": sqltypes.Boolean,
    "D": sqltypes.Date,
    "T": sqltypes.DateTime,
    "C": sqltypes.String,
    "M": sqltypes.Text,
    "B": sqltypes.LargeBinary,
    "I": sqltypes.Integer,
    "G": sqltypes.LargeBinary,
    "V": sqltypes.Text,
    "X": sqltypes.Text,
    "Y": sqltypes.Text,
    "P": sqltypes.Numeric,
    "integer": INTEGER,
    "bigint": BIGINT,
    "smallint": SMALLINT,
    "character varying": VARCHAR,
    "character": CHAR,
    '"char"': sqltypes.String,
    "name": sqltypes.String,
    "text": TEXT,
    "decimal": CustomDecimal,
    "DECIMAL": CustomDecimal,
    "numeric": CustomDecimal,
    "float": sqlalchemy.FLOAT,
    "real": sqlalchemy.REAL,
    "double precision": sqlalchemy.DOUBLE_PRECISION,
    "timestamp": sqlalchemy.TIMESTAMP,
    "timestamp with time zone": sqlalchemy.TIMESTAMP,
    "timestamp without time zone": sqlalchemy.TIMESTAMP,
    "time with time zone": sqlalchemy.TIME,
    "time without time zone": sqlalchemy.TIME,
    "date": sqlalchemy.DATE,
    "time": sqlalchemy.TIME,
    "boolean": sqlalchemy.BOOLEAN,
    "interval": CustomInterval,
    "INTERVAL": CustomInterval,
}

colspecs = {
    sqltypes.Integer: CustomInteger,
    sqltypes.Numeric: NUMERIC,
    sqltypes.Float: CustomDecimal,
    sqltypes.Double: CustomDecimal,
    sqltypes.String: VARCHAR,
    sqltypes.DECIMAL: CustomDecimal,
    sqltypes.Boolean: sqltypes.Boolean,
    sqltypes.Date: sqltypes.Date,
    sqltypes.Time: sqltypes.Time,
    sqltypes.Text: TEXT,
    sqltypes.DateTime: DateTime,
    sqltypes.Interval: CustomInterval,
}




type_map = {
    "C": String,
    "N": Integer,
    "F": Float,
    "D": DateTime,
    "L": Integer,  # Assuming logical type to integer mapping
}


class VFPIdentifierPreparer(compiler.IdentifierPreparer):
    """
    VFP identifier preparer
    """

    reserved_words = {
        "add",
        "all",
        "alter",
        "and",
        "any",
        "as",
        "asc",
        "avg",
        "begin",
        "between",
        "by",
        "case",
        "cast",
        "character",
        "close",
        "commit",
        "count",
        "create",
        "cursor",
        "date",
        "datetime",
        "declare",
        "delete",
        "desc",
        "distinct",
        "drop",
        "end",
        "escape",
        "exists",
        "fetch",
        "for",
        "from",
        "function",
        "group_tag",
        "having",
        "if",
        "in",
        "inner",
        "insert",
        "into",
        "is",
        "join",
        "left",
        "like",
        "max",
        "min",
        "no",
        "not",
        "null",
        "or",
        "order",
        "outer",
        "parameter",
        "right",
        "rollback",
        "select",
        "set",
        "some",
        "sum",
        "table",
        "union",
        "update",
        "values",
        "view",
        "where",
        "while",
    }


_CT = TypeVar("_CT", bound=TypeDecorator)  # Custom Type Variable


class VFPCompiler(compiler.SQLCompiler):
    """
    VFP compiler for SQL statements, this is the main class that needs to be modified.
    """

    def label_select_column(self, select, column, asfrom):
        if isinstance(column, elements.Label):
            return column.name

        if not isinstance(column, elements.ColumnClause):
            return None

        # Customize the aliasing here to include the table name as a prefix
        return f"{column.table.name}_{column.name}"

    def visit_column(self, column, **kwargs):
        # If the column is associated with a table, prefix the column name with the table name
        if column.table is not None:
            rendered_column = f"{column.table.name}.{column.name}"
        else:
            rendered_column = column.name

        return rendered_column

    def visit_table(
            self,
            table,
            asfrom=False,
            iscrud=False,
            ashint=False,
            fromhints=None,
            use_schema=False,
            **kwargs,
    ):
        # Assuming no aliasing, prefixing or other complex transformations are needed
        rendered_table = table.name

        # Add self-aliasing for tables
        if asfrom:
            rendered_table = f"{table.name} {table.name}"

        return rendered_table

    def visit_select(self, select, **kwargs):
        # Call the original visit_select to get the default behavior

        # select.compiled_params
        if select.__dict__.get("_label_style"):
            select.__dict__["_label_style"] = select.__dict__["_label_style"].__class__.LABEL_STYLE_TABLENAME_PLUS_COL
        result = super().visit_select(select, **kwargs)

        return result

    def visit_alias(self, select, **kw):
        # Your custom logic here to modify compiled_params or positiontup
        return super().visit_alias(select, **kw)

    def visit_interval(self, type_, **kw):
        return "MY_CUSTOM_INTERVAL"

    def _process_parameters_for_postcompile(self, parameters, **kwargs):
        result = super()._process_parameters_for_postcompile(parameters, **kwargs)
        return result

    def visit_cast(self, element, **kw):
        target_type = str(element.typeclause.type.dialect_impl(self.dialect))
        value = self.process(element.clause, **kw)

        if "ABS(" in value.upper():
            return value

        if target_type.upper() == "VARCHAR":
            return f"Str({value})"
        elif target_type.upper() == "INTEGER":
            return f"Val({value})"
        elif target_type.upper() == "FLOAT":
            return f"Val({value})"
        elif target_type.upper() == "NUMERIC":
            return f"Val({value})"
        # Add more types here based on your needs
        else:
            # Default action if type is not recognized
            return value

    def visit_binary(self, binary, **kw):
        operator = binary.operator
        left = binary.left
        right = binary.right
        if operator == "-":
            if isinstance(left.type, DateTime) and isinstance(right.type, DateTime):
                # Handle the date subtraction logic as per your custom dialect
                return self.process(left, **kw) + " - " + self.process(right, **kw)

        return super(VFPCompiler, self).visit_binary(binary, **kw)

    def visit_func(self, fn, **kw):
        if fn.name.lower() == 'pow':
            args = list(fn.clauses)
            base, exp = args[0], args[1]
            if base == 10 or base == 5:
                return f"{self.process(base)} ^ {self.process(exp)}"

        return super(VFPCompiler, self).visit_func(fn, **kw)

    def visit_INTERVAL(self, type_, **kw):
        pass


class VFPTypeCompiler(compiler.GenericTypeCompiler):
    """
    VFP type compiler for SQL statements, this will be used to map SQLAlchemy types to VFP types.
    """

    def visit_string(self, type_, **kwargs):
        return "C"

    def visit_integer(self, type_, **kwargs):
        return "N"

    def visit_float(self, type_, **kwargs):
        return "F"

    def visit_datetime(self, type_, **kwargs):
        return "D"

    # Custom handler for your logical to integer mapping
    def visit_logical(self, type_, **kwargs):
        return "L"

    def visit_numeric(self, type_, **kw):
        return self.visit_NUMERIC(type_, **kw)

    def visit_INTERVAL(self, type_, **kw):
        return self.visit_NUMERIC(type_, **kw)

    def visit_interval(self, type_, **kw):
        return self.visit_NUMERIC(type_, **kw)

    def visit_NUMERIC(self, type_, **kw):
        if type_.precision is None:
            return "N"
        elif type_.scale is None:
            return "F"
        else:
            return "F"


class VFPDialect(default.DefaultDialect):
    name = "vfp"
    driver = "pyodbc"
    supports_native_decimal = False
    supports_alter = False
    supports_pk_autoincrement = False
    supports_default_values = False
    supports_empty_insert = False
    supports_unicode_statements = True
    supports_unicode_binds = True
    returns_unicode_strings = True
    description_encoding = None
    supports_native_boolean = False
    preparer = VFPIdentifierPreparer
    statement_compiler = VFPCompiler
    type_compiler = VFPTypeCompiler
    colspecs = colspecs
    ischema_names = ischema_names

    def __init__(self, **kwargs):
        default.DefaultDialect.__init__(self, **kwargs)

    @classmethod
    def import_dbapi(cls):
        # old:  return pyodbc
        return dbapi_stub

    def do_execute(self, cursor, statement, parameters, context=None):
        query = convert_query_for_vfp(statement, parameters)
        cursor.execute(query)

    def do_execute_no_params(self, cursor, statement, context=None):
        query = convert_query_for_vfp(statement)
        cursor.execute(query)

    def do_rollback(self, dbapi_connection):
        pass  # Override to prevent rollback

    def do_commit(self, dbapi_connection):
        pass  # Override to prevent commit

    def do_begin_twophase(self, connection, xid):
        pass  # Override to prevent two-phase commit

    def do_prepare_twophase(self, connection, xid):
        pass  # Override to prevent two-phase commit

    def do_rollback_twophase(self, connection, xid, is_prepared=True, recover=False):
        pass  # Override to prevent two-phase commit

    def do_commit_twophase(self, connection, xid, is_prepared=True, recover=False):
        pass  # Override to prevent two-phase commit

    def get_columns(self, connection, table_name, schema=None, **kwargs):
        query = f'SELECT * FROM "{table_name}" LIMIT 0'
        result = connection.execute(query)
        return [
            {
                "name": col[0],
                "type": type_map[col[1].value],
                "nullable": True,
                "default": None,
            }
            for col in result._cursor_description()
        ]

    def get_columns(self, connection, table_name, schema=None, **kwargs):
        # Since the VFP SQL syntax might differ, you may need to modify the query string accordingly
        query = 'SELECT * FROM "{table}" WHERE .F.'.format(
            table=table_name
        )  # VFP for "WHERE FALSE"
        result = connection.execute(query)

        try:
            cursor_description = result.cursor.description
        except AttributeError:
            cursor_description = []

        return [
            {
                "name": col[0],
                "type": type_map.get(
                    col[1], TrimmedString
                ),  # Default to String if type not found
                "nullable": True,  # VFP nullability info might need a separate query
                "default": None,  # VFP default value might need a separate query
            }
            for col in cursor_description
        ]


registry.register("vfp", "pyvfp64.dialect", "VFPDialect")

def connect(connection_string: str) -> VFPConnection:
    return _vfp_connect(connection_string)           # <-- returns VFPConnection


def make_sessions():
    """
    Create a new session factory for VFP database connections.
    """

    vfp_engine = create_engine(
        "vfp://",
        creator=connect,
        poolclass=pool.SingletonThreadPool,  # Consider SingletonThreadPool for thread-safety

    )

    vfp_session_factory = sessionmaker(
        bind=vfp_engine,
        autocommit=False,  # Do not auto-commit transactions
        expire_on_commit=False,  # Do not expire objects when the transaction ends
    )

    vdb_session = scoped_session(vfp_session_factory)

    return vdb_session
