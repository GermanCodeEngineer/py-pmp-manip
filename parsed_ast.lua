{
    type: "Program",
    sourceType: "script",
    body: [
        {
            type: "ExpressionStatement",
            expression: {
                type: "CallExpression",
                callee: {
                    type: "ArrowFunctionExpression",
                    generator: False,
                    isAsync: False,
                    params: [
                        {
                            type: "Identifier",
                            name: "Scratch"
                        }
                    ],
                    body: {
                        type: "BlockStatement",
                        body: [
                            {
                                type: "ExpressionStatement",
                                expression: {
                                    type: "Literal",
                                    value: "use strict",
                                    raw: "\"use strict\""
                                },
                                directive: "use strict"
                            },
                            {
                                type: "ClassDeclaration",
                                id: {
                                    type: "Identifier",
                                    name: "DumbExample"
                                },
                                body: {
                                    type: "ClassBody",
                                    body: [
                                        {
                                            type: "MethodDefinition",
                                            key: {
                                                type: "Identifier",
                                                name: "getInfo"
                                            },
                                            computed: False,
                                            value: {
                                                type: "FunctionExpression",
                                                expression: False,
                                                isAsync: False,
                                                params: [],
                                                body: {
                                                    type: "BlockStatement",
                                                    body: [
                                                        {
                                                            type: "ReturnStatement",
                                                            argument: {
                                                                type: "ObjectExpression",
                                                                properties: [
                                                                    {
                                                                        type: "Property",
                                                                        key: {
                                                                            type: "Identifier",
                                                                            name: "id"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "Literal",
                                                                            value: "dumbExample",
                                                                            raw: "\"dumbExample\""
                                                                        },
                                                                        kind: "init",
                                                                        method: False,
                                                                        shorthand: False
                                                                    },
                                                                    {
                                                                        type: "Property",
                                                                        key: {
                                                                            type: "Identifier",
                                                                            name: "name"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "Literal",
                                                                            value: "Dumb Example",
                                                                            raw: "\"Dumb Example\""
                                                                        },
                                                                        kind: "init",
                                                                        method: False,
                                                                        shorthand: False
                                                                    },
                                                                    {
                                                                        type: "Property",
                                                                        key: {
                                                                            type: "Identifier",
                                                                            name: "color1"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "Literal",
                                                                            value: "#e200ca",
                                                                            raw: "\"#e200ca\""
                                                                        },
                                                                        kind: "init",
                                                                        method: False,
                                                                        shorthand: False
                                                                    },
                                                                    {
                                                                        type: "Property",
                                                                        key: {
                                                                            type: "Identifier",
                                                                            name: "blocks"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "ArrayExpression",
                                                                            elements: [
                                                                                {
                                                                                    type: "ObjectExpression",
                                                                                    properties: [
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "opcode"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "Literal",
                                                                                                value: "last_used_base",
                                                                                                raw: "\"last_used_base\""
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "blockType"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "MemberExpression",
                                                                                                computed: False,
                                                                                                object: {
                                                                                                    type: "MemberExpression",
                                                                                                    computed: False,
                                                                                                    object: {
                                                                                                        type: "Identifier",
                                                                                                        name: "Scratch"
                                                                                                    },
                                                                                                    property: {
                                                                                                        type: "Identifier",
                                                                                                        name: "BlockType"
                                                                                                    }
                                                                                                },
                                                                                                property: {
                                                                                                    type: "Identifier",
                                                                                                    name: "REPORTER"
                                                                                                }
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "text"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "Literal",
                                                                                                value: "last used base",
                                                                                                raw: "\"last used base\""
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "arguments"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "ObjectExpression",
                                                                                                properties: []
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    type: "ObjectExpression",
                                                                                    properties: [
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "opcode"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "Literal",
                                                                                                value: "last_two_inout_values",
                                                                                                raw: "\"last_two_inout_values\""
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "blockType"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "MemberExpression",
                                                                                                computed: False,
                                                                                                object: {
                                                                                                    type: "MemberExpression",
                                                                                                    computed: False,
                                                                                                    object: {
                                                                                                        type: "Identifier",
                                                                                                        name: "Scratch"
                                                                                                    },
                                                                                                    property: {
                                                                                                        type: "Identifier",
                                                                                                        name: "BlockType"
                                                                                                    }
                                                                                                },
                                                                                                property: {
                                                                                                    type: "Identifier",
                                                                                                    name: "REPORTER"
                                                                                                }
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "text"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "Literal",
                                                                                                value: "last two [S1] and [S2] values",
                                                                                                raw: "\"last two [S1] and [S2] values\""
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        },
                                                                                        {
                                                                                            type: "Property",
                                                                                            key: {
                                                                                                type: "Identifier",
                                                                                                name: "arguments"
                                                                                            },
                                                                                            computed: False,
                                                                                            value: {
                                                                                                type: "ObjectExpression",
                                                                                                properties: [
                                                                                                    {
                                                                                                        type: "Property",
                                                                                                        key: {
                                                                                                            type: "Identifier",
                                                                                                            name: "S1"
                                                                                                        },
                                                                                                        computed: False,
                                                                                                        value: {
                                                                                                            type: "ObjectExpression",
                                                                                                            properties: [
                                                                                                                {
                                                                                                                    type: "Property",
                                                                                                                    key: {
                                                                                                                        type: "Identifier",
                                                                                                                        name: "type"
                                                                                                                    },
                                                                                                                    computed: False,
                                                                                                                    value: {
                                                                                                                        type: "MemberExpression",
                                                                                                                        computed: False,
                                                                                                                        object: {
                                                                                                                            type: "MemberExpression",
                                                                                                                            computed: False,
                                                                                                                            object: {
                                                                                                                                type: "Identifier",
                                                                                                                                name: "Scratch"
                                                                                                                            },
                                                                                                                            property: {
                                                                                                                                type: "Identifier",
                                                                                                                                name: "ArgumentType"
                                                                                                                            }
                                                                                                                        },
                                                                                                                        property: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "STRING"
                                                                                                                        }
                                                                                                                    },
                                                                                                                    kind: "init",
                                                                                                                    method: False,
                                                                                                                    shorthand: False
                                                                                                                },
                                                                                                                {
                                                                                                                    type: "Property",
                                                                                                                    key: {
                                                                                                                        type: "Identifier",
                                                                                                                        name: "menu"
                                                                                                                    },
                                                                                                                    computed: False,
                                                                                                                    value: {
                                                                                                                        type: "Literal",
                                                                                                                        value: "in_out_menue",
                                                                                                                        raw: "\"in_out_menue\""
                                                                                                                    },
                                                                                                                    kind: "init",
                                                                                                                    method: False,
                                                                                                                    shorthand: False
                                                                                                                }
                                                                                                            ]
                                                                                                        },
                                                                                                        kind: "init",
                                                                                                        method: False,
                                                                                                        shorthand: False
                                                                                                    },
                                                                                                    {
                                                                                                        type: "Property",
                                                                                                        key: {
                                                                                                            type: "Identifier",
                                                                                                            name: "S2"
                                                                                                        },
                                                                                                        computed: False,
                                                                                                        value: {
                                                                                                            type: "ObjectExpression",
                                                                                                            properties: [
                                                                                                                {
                                                                                                                    type: "Property",
                                                                                                                    key: {
                                                                                                                        type: "Identifier",
                                                                                                                        name: "type"
                                                                                                                    },
                                                                                                                    computed: False,
                                                                                                                    value: {
                                                                                                                        type: "MemberExpression",
                                                                                                                        computed: False,
                                                                                                                        object: {
                                                                                                                            type: "MemberExpression",
                                                                                                                            computed: False,
                                                                                                                            object: {
                                                                                                                                type: "Identifier",
                                                                                                                                name: "Scratch"
                                                                                                                            },
                                                                                                                            property: {
                                                                                                                                type: "Identifier",
                                                                                                                                name: "ArgumentType"
                                                                                                                            }
                                                                                                                        },
                                                                                                                        property: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "STRING"
                                                                                                                        }
                                                                                                                    },
                                                                                                                    kind: "init",
                                                                                                                    method: False,
                                                                                                                    shorthand: False
                                                                                                                },
                                                                                                                {
                                                                                                                    type: "Property",
                                                                                                                    key: {
                                                                                                                        type: "Identifier",
                                                                                                                        name: "menu"
                                                                                                                    },
                                                                                                                    computed: False,
                                                                                                                    value: {
                                                                                                                        type: "Literal",
                                                                                                                        value: "in_out_menue",
                                                                                                                        raw: "\"in_out_menue\""
                                                                                                                    },
                                                                                                                    kind: "init",
                                                                                                                    method: False,
                                                                                                                    shorthand: False
                                                                                                                }
                                                                                                            ]
                                                                                                        },
                                                                                                        kind: "init",
                                                                                                        method: False,
                                                                                                        shorthand: False
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            kind: "init",
                                                                                            method: False,
                                                                                            shorthand: False
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        },
                                                                        kind: "init",
                                                                        method: False,
                                                                        shorthand: False
                                                                    },
                                                                    {
                                                                        type: "Property",
                                                                        key: {
                                                                            type: "Identifier",
                                                                            name: "menus"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "ObjectExpression",
                                                                            properties: [
                                                                                {
                                                                                    type: "Property",
                                                                                    key: {
                                                                                        type: "Identifier",
                                                                                        name: "in_out_menue"
                                                                                    },
                                                                                    computed: False,
                                                                                    value: {
                                                                                        type: "ObjectExpression",
                                                                                        properties: [
                                                                                            {
                                                                                                type: "Property",
                                                                                                key: {
                                                                                                    type: "Identifier",
                                                                                                    name: "acceptReporters"
                                                                                                },
                                                                                                computed: False,
                                                                                                value: {
                                                                                                    type: "Literal",
                                                                                                    value: False,
                                                                                                    raw: "false"
                                                                                                },
                                                                                                kind: "init",
                                                                                                method: False,
                                                                                                shorthand: False
                                                                                            },
                                                                                            {
                                                                                                type: "Property",
                                                                                                key: {
                                                                                                    type: "Identifier",
                                                                                                    name: "items"
                                                                                                },
                                                                                                computed: False,
                                                                                                value: {
                                                                                                    type: "ArrayExpression",
                                                                                                    elements: [
                                                                                                        {
                                                                                                            type: "Literal",
                                                                                                            value: "IN",
                                                                                                            raw: "\"IN\""
                                                                                                        },
                                                                                                        {
                                                                                                            type: "Literal",
                                                                                                            value: "OUT",
                                                                                                            raw: "\"OUT\""
                                                                                                        }
                                                                                                    ]
                                                                                                },
                                                                                                kind: "init",
                                                                                                method: False,
                                                                                                shorthand: False
                                                                                            }
                                                                                        ]
                                                                                    },
                                                                                    kind: "init",
                                                                                    method: False,
                                                                                    shorthand: False
                                                                                }
                                                                            ]
                                                                        },
                                                                        kind: "init",
                                                                        method: False,
                                                                        shorthand: False
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                },
                                                generator: False
                                            },
                                            kind: "method",
                                            static: False
                                        },
                                        {
                                            type: "MethodDefinition",
                                            key: {
                                                type: "Identifier",
                                                name: "last_used_base"
                                            },
                                            computed: False,
                                            value: {
                                                type: "FunctionExpression",
                                                expression: False,
                                                isAsync: False,
                                                params: [],
                                                body: {
                                                    type: "BlockStatement",
                                                    body: [
                                                        {
                                                            type: "ReturnStatement",
                                                            argument: {
                                                                type: "Literal",
                                                                value: "some base",
                                                                raw: "\"some base\""
                                                            }
                                                        }
                                                    ]
                                                },
                                                generator: False
                                            },
                                            kind: "method",
                                            static: False
                                        },
                                        {
                                            type: "MethodDefinition",
                                            key: {
                                                type: "Identifier",
                                                name: "last_two_inout_values"
                                            },
                                            computed: False,
                                            value: {
                                                type: "FunctionExpression",
                                                expression: False,
                                                isAsync: False,
                                                params: [
                                                    {
                                                        type: "ObjectPattern",
                                                        properties: [
                                                            {
                                                                type: "Property",
                                                                key: {
                                                                    type: "Identifier",
                                                                    name: "S1"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "S1"
                                                                },
                                                                kind: "init",
                                                                method: False,
                                                                shorthand: True
                                                            },
                                                            {
                                                                type: "Property",
                                                                key: {
                                                                    type: "Identifier",
                                                                    name: "S2"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "S2"
                                                                },
                                                                kind: "init",
                                                                method: False,
                                                                shorthand: True
                                                            }
                                                        ]
                                                    }
                                                ],
                                                body: {
                                                    type: "BlockStatement",
                                                    body: [
                                                        {
                                                            type: "ReturnStatement",
                                                            argument: {
                                                                type: "CallExpression",
                                                                callee: {
                                                                    type: "MemberExpression",
                                                                    computed: False,
                                                                    object: {
                                                                        type: "Identifier",
                                                                        name: "JSON"
                                                                    },
                                                                    property: {
                                                                        type: "Identifier",
                                                                        name: "stringify"
                                                                    }
                                                                },
                                                                arguments: [
                                                                    {
                                                                        type: "ArrayExpression",
                                                                        elements: [
                                                                            {
                                                                                type: "Literal",
                                                                                value: "HERE",
                                                                                raw: "\"HERE\""
                                                                            },
                                                                            {
                                                                                type: "Identifier",
                                                                                name: "S1"
                                                                            },
                                                                            {
                                                                                type: "Identifier",
                                                                                name: "S2"
                                                                            }
                                                                        ]
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                },
                                                generator: False
                                            },
                                            kind: "method",
                                            static: False
                                        }
                                    ]
                                }
                            },
                            {
                                type: "ExpressionStatement",
                                expression: {
                                    type: "CallExpression",
                                    callee: {
                                        type: "MemberExpression",
                                        computed: False,
                                        object: {
                                            type: "MemberExpression",
                                            computed: False,
                                            object: {
                                                type: "Identifier",
                                                name: "Scratch"
                                            },
                                            property: {
                                                type: "Identifier",
                                                name: "extensions"
                                            }
                                        },
                                        property: {
                                            type: "Identifier",
                                            name: "register"
                                        }
                                    },
                                    arguments: [
                                        {
                                            type: "NewExpression",
                                            callee: {
                                                type: "Identifier",
                                                name: "DumbExample"
                                            },
                                            arguments: []
                                        }
                                    ]
                                }
                            },
                            {
                                type: "ExpressionStatement",
                                expression: {
                                    type: "CallExpression",
                                    callee: {
                                        type: "MemberExpression",
                                        computed: False,
                                        object: {
                                            type: "Identifier",
                                            name: "console"
                                        },
                                        property: {
                                            type: "Identifier",
                                            name: "log"
                                        }
                                    },
                                    arguments: [
                                        {
                                            type: "Identifier",
                                            name: "Scratch"
                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    expression: False
                },
                arguments: [
                    {
                        type: "Identifier",
                        name: "Scratch"
                    }
                ]
            }
        }
    ]
}