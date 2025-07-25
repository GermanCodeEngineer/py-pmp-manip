{
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
                value: "asyncexample",
                raw: "'asyncexample'"
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
                value: "Async Blocks",
                raw: "'Async Blocks'"
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
                                    value: "wait",
                                    raw: "'wait'"
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
                                    value: "wait [TIME] seconds",
                                    raw: "'wait [TIME] seconds'"
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
                                        name: "COMMAND"
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
                                                name: "TIME"
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
                                                                name: "NUMBER"
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
                                                            name: "defaultValue"
                                                        },
                                                        computed: False,
                                                        value: {
                                                            type: "Literal",
                                                            value: 1,
                                                            raw: "1"
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
                                    value: "fetch",
                                    raw: "'fetch'"
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
                                    value: "fetch [URL]",
                                    raw: "'fetch [URL]'"
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
                                                name: "URL"
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
                                                            name: "defaultValue"
                                                        },
                                                        computed: False,
                                                        value: {
                                                            type: "Literal",
                                                            value: "https://extensions.turbowarp.org/hello.txt",
                                                            raw: "'https://extensions.turbowarp.org/hello.txt'"
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
        }
    ]
}