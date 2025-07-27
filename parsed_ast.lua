{
    type: "Program",
    sourceType: "script",
    body: [
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
                            name: "translate"
                        }
                    },
                    property: {
                        type: "Identifier",
                        name: "setup"
                    }
                },
                arguments: [
                    {
                        type: "ObjectExpression",
                        properties: [
                            {
                                type: "Property",
                                key: {
                                    type: "Literal",
                                    value: "de",
                                    raw: "\"de\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "Basis",
                                                raw: "\"Basis\""
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
                                    type: "Literal",
                                    value: "fi",
                                    raw: "\"fi\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "Kantaluvut",
                                                raw: "\"Kantaluvut\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A] kantaluvusta [B] kantalukuun [C]",
                                                raw: "\"[A] kantaluvusta [B] kantalukuun [C]\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "onko luvun [A] kantaluku [B]?",
                                                raw: "\"onko luvun [A] kantaluku [B]?\""
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
                                    type: "Literal",
                                    value: "it",
                                    raw: "\"it\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "Basi",
                                                raw: "\"Basi\""
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
                                    type: "Literal",
                                    value: "ja",
                                    raw: "\"ja\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\u9032\u6570",
                                                raw: "\"\u9032\u6570\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[B]\u9032\u6570\u306e\u6570[A]\u3092[C]\u9032\u6570\u306b\u5909\u63db\u3059\u308b",
                                                raw: "\"[B]\u9032\u6570\u306e\u6570[A]\u3092[C]\u9032\u6570\u306b\u5909\u63db\u3059\u308b\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A]\u306f[B]\u9032\u6570\u3067\u8868\u73fe\u3067\u304d\u308b",
                                                raw: "\"[A]\u306f[B]\u9032\u6570\u3067\u8868\u73fe\u3067\u304d\u308b\""
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
                                    type: "Literal",
                                    value: "ko",
                                    raw: "\"ko\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\uc9c4\ubc95",
                                                raw: "\"\uc9c4\ubc95\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A]\uc744(\ub97c) [B]\uc9c4\ubc95\uc5d0\uc11c [C]\uc9c4\ubc95\uc73c\ub85c",
                                                raw: "\"[A]\uc744(\ub97c) [B]\uc9c4\ubc95\uc5d0\uc11c [C]\uc9c4\ubc95\uc73c\ub85c\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A](\uc774)\uac00 [B]\uc9c4\ubc95\uc778\uac00?",
                                                raw: "\"[A](\uc774)\uac00 [B]\uc9c4\ubc95\uc778\uac00?\""
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
                                    type: "Literal",
                                    value: "nb",
                                    raw: "\"nb\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A] fra base [B] til base [C]",
                                                raw: "\"[A] fra base [B] til base [C]\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "er base [B] [A]?",
                                                raw: "\"er base [B] [A]?\""
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
                                    type: "Literal",
                                    value: "nl",
                                    raw: "\"nl\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "zet [A] om van base-[B] naar base-[C]",
                                                raw: "\"zet [A] om van base-[B] naar base-[C]\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "is [A] base-[B]?",
                                                raw: "\"is [A] base-[B]?\""
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
                                    type: "Literal",
                                    value: "ru",
                                    raw: "\"ru\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\u0411\u0430\u0437\u0430",
                                                raw: "\"\u0411\u0430\u0437\u0430\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A] \u0438\u0437 \u0431\u0430\u0437\u044b [B] \u0432 \u0431\u0430\u0437\u0443 [C]",
                                                raw: "\"[A] \u0438\u0437 \u0431\u0430\u0437\u044b [B] \u0432 \u0431\u0430\u0437\u0443 [C]\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\u0431\u0430\u0437\u0430 [B] [A]?",
                                                raw: "\"\u0431\u0430\u0437\u0430 [B] [A]?\""
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
                                    type: "Literal",
                                    value: "zh-cn",
                                    raw: "\"zh-cn\""
                                },
                                computed: False,
                                value: {
                                    type: "ObjectExpression",
                                    properties: [
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_Base",
                                                raw: "\"_Base\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\u8fdb\u5236\u8f6c\u6362",
                                                raw: "\"\u8fdb\u5236\u8f6c\u6362\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_[A] from base [B] to base [C]",
                                                raw: "\"_[A] from base [B] to base [C]\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "\u628a[B]\u8fdb\u5236\u7684[A]\u8f6c\u6362\u6210[C]",
                                                raw: "\"\u628a[B]\u8fdb\u5236\u7684[A]\u8f6c\u6362\u6210[C]\""
                                            },
                                            kind: "init",
                                            method: False,
                                            shorthand: False
                                        },
                                        {
                                            type: "Property",
                                            key: {
                                                type: "Literal",
                                                value: "_is base [B] [A]?",
                                                raw: "\"_is base [B] [A]?\""
                                            },
                                            computed: False,
                                            value: {
                                                type: "Literal",
                                                value: "[A]\u662f[B]\u8fdb\u5236\u5417\uff1f",
                                                raw: "\"[A]\u662f[B]\u8fdb\u5236\u5417\uff1f\""
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
            }
        },
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
                                type: "VariableDeclaration",
                                declarations: [
                                    {
                                        type: "VariableDeclarator",
                                        id: {
                                            type: "Identifier",
                                            name: "icon"
                                        },
                                        init: {
                                            type: "Literal",
                                            value: "data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHdpZHRoPSIyMjUuMzU0OCIgaGVpZ2h0PSIyMjUuMzU0OCIgdmlld0JveD0iMCwwLDIyNS4zNTQ4LDIyNS4zNTQ4Ij48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTg3LjMyMjk0LC0zNy4zMjI1OSkiPjxnIGRhdGEtcGFwZXItZGF0YT0ieyZxdW90O2lzUGFpbnRpbmdMYXllciZxdW90Ozp0cnVlfSIgc3Ryb2tlLWxpbmVqb2luPSJtaXRlciIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBzdHJva2UtZGFzaGFycmF5PSIiIHN0cm9rZS1kYXNob2Zmc2V0PSIwIiBzdHlsZT0ibWl4LWJsZW5kLW1vZGU6IG5vcm1hbCI+PHBhdGggZD0iTTE4Ny4zMjI5NCwxNTBjMCwtNjIuMjMwMDEgNTAuNDQ3MzksLTExMi42Nzc0IDExMi42Nzc0LC0xMTIuNjc3NGM2Mi4yMzAwMSwwIDExMi42Nzc0LDUwLjQ0NzM5IDExMi42Nzc0LDExMi42Nzc0YzAsNjIuMjMwMDEgLTUwLjQ0NzM5LDExMi42Nzc0IC0xMTIuNjc3NCwxMTIuNjc3NGMtNjIuMjMwMDEsMCAtMTEyLjY3NzQsLTUwLjQ0NzM5IC0xMTIuNjc3NCwtMTEyLjY3NzR6IiBmaWxsPSIjZTIwMGNhIiBmaWxsLXJ1bGU9Im5vbnplcm8iIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIwIiBzdHJva2UtbGluZWNhcD0iYnV0dCIvPjxnIGZpbGw9IiNmZmZmZmYiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSI1Ij48cGF0aCBkPSJNMzI1LjA1LDE3My41MDAyMXYxMi43aC00OS45di0xMC41bDE3LjksLTE4LjFjMy42LC0zLjczMzM0IDYuNSwtNi44NSA4LjcsLTkuMzVjMC43NDQyOSwtMC44NDIxNiAxLjQ1Nzc2LC0xLjcxMTA2IDIuMTM5LC0yLjYwNWMxLjEzMzMzLC0xLjQ5NDY2IDIuMDIwMzMsLTIuODkzIDIuNjYxLC00LjE5NWMxLC0yLjAzMzMzIDEuNSwtNC4yMTY2NyAxLjUsLTYuNTVjMCwtMi44NjY2NyAtMC43ODMzMywtNSAtMi4zNSwtNi40Yy0wLjk3ODg1LC0wLjg2MTMzIC0yLjE1NDg0LC0xLjQ2ODIyIC0zLjQyNCwtMS43NjdjLTAuODA0NjYsLTAuMjAxMzQgLTEuNjgxLC0wLjMxMTY3IC0yLjYyOSwtMC4zMzFjLTAuMDk4OTksLTAuMDAxNjUgLTAuMTk4LC0wLjAwMjMyIC0wLjI5NywtMC4wMDJjLTIuNjg1OTQsMC4wMDg2MSAtNS4zMzU5NSwwLjYxNzgyIC03Ljc1NiwxLjc4M2MtMC4wODE1OCwwLjAzODQ3IC0wLjE2MjkyLDAuMDc3NDcgLTAuMjQ0LDAuMTE3Yy0xLjI5MDA4LDAuNjM0MDggLTIuNTQwMzksMS4zNDYwNyAtMy43NDQsMi4xMzJjLTEuMjIxMzQsMC43OTIgLTIuNDY5NjYsMS42OTEzNCAtMy43NDUsMi42OThjLTAuMjM4NDMsMC4xODgyMSAtMC40NzU0MywwLjM3ODIxIC0wLjcxMSwwLjU3bC04LjIsLTkuN2MyLjA2NjY2LC0xLjggNC4yNSwtMy40NjY2NyA2LjU1LC01YzEuNDk5MTksLTAuOTkxNTMgMy4wODY1OCwtMS44NDI3OSA0Ljc0MiwtMi41NDNjMS4wNjYxNywtMC40NTM5NSAyLjE1MzQxLC0wLjg1Njc1IDMuMjU4LC0xLjIwN2MzLjAzMzMzLC0wLjk2NjY3IDYuNjgzMzQsLTEuNDUgMTAuOTUsLTEuNDVjMS45MjgwNywtMC4wMDk4MyAzLjg1MzE0LDAuMTUzNDkgNS43NTIsMC40ODhjMi4yODY2NywwLjQxNDY2IDQuMzcxMzMsMS4wOTQzMyA2LjI1NCwyLjAzOWMwLjAxNDY4LDAuMDA3NjUgMC4wMjkzNSwwLjAxNTMyIDAuMDQ0LDAuMDIzYzEuODM0NjIsMC45MDk4IDMuNTIzNzYsMi4wODczNCA1LjAxMiwzLjQ5NGMxLjA2NDkxLDEuMDE3MjUgMi4wMDEyMiwyLjE2MTA5IDIuNzg4LDMuNDA2YzEuODMzMzMsMi45IDIuNzUsNi4xODMzNCAyLjc1LDkuODVjMC4wMTUwNCwyLjQ3MzU4IC0wLjMyNTc4LDQuOTM2NDYgLTEuMDEyLDcuMzEzYy0wLjM1MTQxLDEuMTk2NDYgLTAuNzk4ODYsMi4zNjI1OCAtMS4zMzgsMy40ODdjLTAuOTMzMywxLjkyMzY5IC0yLjA0MDU4LDMuNzU4IC0zLjMwOCw1LjQ4Yy0xLjA4MDI3LDEuNDczOSAtMi4yNDYyOSwyLjg4MyAtMy40OTIsNC4yMmMtMS4zODY3NCwxLjQ5MTY5IC0yLjgwMzAyLDIuOTU1NjUgLTQuMjQ4LDQuMzkxYy0xLjQ3OTMzLDEuNDczMzMgLTMuMDY4MzMsMy4wMDU2NyAtNC43NjcsNC41OTdjLTAuNTc1OTcsMC41Mzk4NyAtMS4xNTQzMSwxLjA3NzIxIC0xLjczNSwxLjYxMmwtOS4yLDguNnYwLjd6IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjxnIGZpbGwtcnVsZT0ibm9uemVybyIgc3Ryb2tlLWxpbmVjYXA9ImJ1dHQiPjxwYXRoIGQ9Ik0yMzYuNzUsODYuNzVoMTI2LjV2MTIuNTk3OTJoLTEyNi41eiIvPjxwYXRoIGQ9Ik0yNDkuMzQ3OTIsODYuNzV2MTI2LjVoLTEyLjU5Nzkydi0xMjYuNXoiLz48L2c+PC9nPjwvZz48L2c+PC9zdmc+PCEtLXJvdGF0aW9uQ2VudGVyOjExMi42NzcwNjAwMDAwMDAwMToxMTIuNjc3NDA1LS0+",
                                            raw: "\"data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHdpZHRoPSIyMjUuMzU0OCIgaGVpZ2h0PSIyMjUuMzU0OCIgdmlld0JveD0iMCwwLDIyNS4zNTQ4LDIyNS4zNTQ4Ij48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTg3LjMyMjk0LC0zNy4zMjI1OSkiPjxnIGRhdGEtcGFwZXItZGF0YT0ieyZxdW90O2lzUGFpbnRpbmdMYXllciZxdW90Ozp0cnVlfSIgc3Ryb2tlLWxpbmVqb2luPSJtaXRlciIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBzdHJva2UtZGFzaGFycmF5PSIiIHN0cm9rZS1kYXNob2Zmc2V0PSIwIiBzdHlsZT0ibWl4LWJsZW5kLW1vZGU6IG5vcm1hbCI+PHBhdGggZD0iTTE4Ny4zMjI5NCwxNTBjMCwtNjIuMjMwMDEgNTAuNDQ3MzksLTExMi42Nzc0IDExMi42Nzc0LC0xMTIuNjc3NGM2Mi4yMzAwMSwwIDExMi42Nzc0LDUwLjQ0NzM5IDExMi42Nzc0LDExMi42Nzc0YzAsNjIuMjMwMDEgLTUwLjQ0NzM5LDExMi42Nzc0IC0xMTIuNjc3NCwxMTIuNjc3NGMtNjIuMjMwMDEsMCAtMTEyLjY3NzQsLTUwLjQ0NzM5IC0xMTIuNjc3NCwtMTEyLjY3NzR6IiBmaWxsPSIjZTIwMGNhIiBmaWxsLXJ1bGU9Im5vbnplcm8iIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIwIiBzdHJva2UtbGluZWNhcD0iYnV0dCIvPjxnIGZpbGw9IiNmZmZmZmYiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSI1Ij48cGF0aCBkPSJNMzI1LjA1LDE3My41MDAyMXYxMi43aC00OS45di0xMC41bDE3LjksLTE4LjFjMy42LC0zLjczMzM0IDYuNSwtNi44NSA4LjcsLTkuMzVjMC43NDQyOSwtMC44NDIxNiAxLjQ1Nzc2LC0xLjcxMTA2IDIuMTM5LC0yLjYwNWMxLjEzMzMzLC0xLjQ5NDY2IDIuMDIwMzMsLTIuODkzIDIuNjYxLC00LjE5NWMxLC0yLjAzMzMzIDEuNSwtNC4yMTY2NyAxLjUsLTYuNTVjMCwtMi44NjY2NyAtMC43ODMzMywtNSAtMi4zNSwtNi40Yy0wLjk3ODg1LC0wLjg2MTMzIC0yLjE1NDg0LC0xLjQ2ODIyIC0zLjQyNCwtMS43NjdjLTAuODA0NjYsLTAuMjAxMzQgLTEuNjgxLC0wLjMxMTY3IC0yLjYyOSwtMC4zMzFjLTAuMDk4OTksLTAuMDAxNjUgLTAuMTk4LC0wLjAwMjMyIC0wLjI5NywtMC4wMDJjLTIuNjg1OTQsMC4wMDg2MSAtNS4zMzU5NSwwLjYxNzgyIC03Ljc1NiwxLjc4M2MtMC4wODE1OCwwLjAzODQ3IC0wLjE2MjkyLDAuMDc3NDcgLTAuMjQ0LDAuMTE3Yy0xLjI5MDA4LDAuNjM0MDggLTIuNTQwMzksMS4zNDYwNyAtMy43NDQsMi4xMzJjLTEuMjIxMzQsMC43OTIgLTIuNDY5NjYsMS42OTEzNCAtMy43NDUsMi42OThjLTAuMjM4NDMsMC4xODgyMSAtMC40NzU0MywwLjM3ODIxIC0wLjcxMSwwLjU3bC04LjIsLTkuN2MyLjA2NjY2LC0xLjggNC4yNSwtMy40NjY2NyA2LjU1LC01YzEuNDk5MTksLTAuOTkxNTMgMy4wODY1OCwtMS44NDI3OSA0Ljc0MiwtMi41NDNjMS4wNjYxNywtMC40NTM5NSAyLjE1MzQxLC0wLjg1Njc1IDMuMjU4LC0xLjIwN2MzLjAzMzMzLC0wLjk2NjY3IDYuNjgzMzQsLTEuNDUgMTAuOTUsLTEuNDVjMS45MjgwNywtMC4wMDk4MyAzLjg1MzE0LDAuMTUzNDkgNS43NTIsMC40ODhjMi4yODY2NywwLjQxNDY2IDQuMzcxMzMsMS4wOTQzMyA2LjI1NCwyLjAzOWMwLjAxNDY4LDAuMDA3NjUgMC4wMjkzNSwwLjAxNTMyIDAuMDQ0LDAuMDIzYzEuODM0NjIsMC45MDk4IDMuNTIzNzYsMi4wODczNCA1LjAxMiwzLjQ5NGMxLjA2NDkxLDEuMDE3MjUgMi4wMDEyMiwyLjE2MTA5IDIuNzg4LDMuNDA2YzEuODMzMzMsMi45IDIuNzUsNi4xODMzNCAyLjc1LDkuODVjMC4wMTUwNCwyLjQ3MzU4IC0wLjMyNTc4LDQuOTM2NDYgLTEuMDEyLDcuMzEzYy0wLjM1MTQxLDEuMTk2NDYgLTAuNzk4ODYsMi4zNjI1OCAtMS4zMzgsMy40ODdjLTAuOTMzMywxLjkyMzY5IC0yLjA0MDU4LDMuNzU4IC0zLjMwOCw1LjQ4Yy0xLjA4MDI3LDEuNDczOSAtMi4yNDYyOSwyLjg4MyAtMy40OTIsNC4yMmMtMS4zODY3NCwxLjQ5MTY5IC0yLjgwMzAyLDIuOTU1NjUgLTQuMjQ4LDQuMzkxYy0xLjQ3OTMzLDEuNDczMzMgLTMuMDY4MzMsMy4wMDU2NyAtNC43NjcsNC41OTdjLTAuNTc1OTcsMC41Mzk4NyAtMS4xNTQzMSwxLjA3NzIxIC0xLjczNSwxLjYxMmwtOS4yLDguNnYwLjd6IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjxnIGZpbGwtcnVsZT0ibm9uemVybyIgc3Ryb2tlLWxpbmVjYXA9ImJ1dHQiPjxwYXRoIGQ9Ik0yMzYuNzUsODYuNzVoMTI2LjV2MTIuNTk3OTJoLTEyNi41eiIvPjxwYXRoIGQ9Ik0yNDkuMzQ3OTIsODYuNzV2MTI2LjVoLTEyLjU5Nzkydi0xMjYuNXoiLz48L2c+PC9nPjwvZz48L2c+PC9zdmc+PCEtLXJvdGF0aW9uQ2VudGVyOjExMi42NzcwNjAwMDAwMDAwMToxMTIuNjc3NDA1LS0+\""
                                        }
                                    }
                                ],
                                kind: "const"
                            },
                            {
                                type: "VariableDeclaration",
                                declarations: [
                                    {
                                        type: "VariableDeclarator",
                                        id: {
                                            type: "Identifier",
                                            name: "cast"
                                        },
                                        init: {
                                            type: "MemberExpression",
                                            computed: False,
                                            object: {
                                                type: "Identifier",
                                                name: "Scratch"
                                            },
                                            property: {
                                                type: "Identifier",
                                                name: "Cast"
                                            }
                                        }
                                    }
                                ],
                                kind: "const"
                            },
                            {
                                type: "VariableDeclaration",
                                declarations: [
                                    {
                                        type: "VariableDeclarator",
                                        id: {
                                            type: "Identifier",
                                            name: "bases"
                                        },
                                        init: {
                                            type: "ArrayExpression",
                                            elements: [
                                                {
                                                    type: "Literal",
                                                    value: "2",
                                                    raw: "\"2\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "3",
                                                    raw: "\"3\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "4",
                                                    raw: "\"4\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "5",
                                                    raw: "\"5\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "6",
                                                    raw: "\"6\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "7",
                                                    raw: "\"7\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "8",
                                                    raw: "\"8\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "9",
                                                    raw: "\"9\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "10",
                                                    raw: "\"10\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "11",
                                                    raw: "\"11\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "12",
                                                    raw: "\"12\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "13",
                                                    raw: "\"13\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "14",
                                                    raw: "\"14\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "15",
                                                    raw: "\"15\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "16",
                                                    raw: "\"16\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "17",
                                                    raw: "\"17\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "18",
                                                    raw: "\"18\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "19",
                                                    raw: "\"19\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "20",
                                                    raw: "\"20\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "21",
                                                    raw: "\"21\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "22",
                                                    raw: "\"22\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "23",
                                                    raw: "\"23\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "24",
                                                    raw: "\"24\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "25",
                                                    raw: "\"25\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "26",
                                                    raw: "\"26\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "27",
                                                    raw: "\"27\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "28",
                                                    raw: "\"28\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "29",
                                                    raw: "\"29\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "30",
                                                    raw: "\"30\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "31",
                                                    raw: "\"31\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "32",
                                                    raw: "\"32\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "33",
                                                    raw: "\"33\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "34",
                                                    raw: "\"34\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "35",
                                                    raw: "\"35\""
                                                },
                                                {
                                                    type: "Literal",
                                                    value: "36",
                                                    raw: "\"36\""
                                                }
                                            ]
                                        }
                                    }
                                ],
                                kind: "const"
                            },
                            {
                                type: "VariableDeclaration",
                                declarations: [
                                    {
                                        type: "VariableDeclarator",
                                        id: {
                                            type: "Identifier",
                                            name: "chars"
                                        },
                                        init: {
                                            type: "Literal",
                                            value: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                            raw: "\"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\""
                                        }
                                    }
                                ],
                                kind: "const"
                            },
                            {
                                type: "ClassDeclaration",
                                id: {
                                    type: "Identifier",
                                    name: "ScratchBase"
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
                                                                            value: "truefantombase",
                                                                            raw: "\"truefantombase\""
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
                                                                            type: "CallExpression",
                                                                            callee: {
                                                                                type: "MemberExpression",
                                                                                computed: False,
                                                                                object: {
                                                                                    type: "Identifier",
                                                                                    name: "Scratch"
                                                                                },
                                                                                property: {
                                                                                    type: "Identifier",
                                                                                    name: "translate"
                                                                                }
                                                                            },
                                                                            arguments: [
                                                                                {
                                                                                    type: "Literal",
                                                                                    value: "Base",
                                                                                    raw: "\"Base\""
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
                                                                            name: "menuIconURI"
                                                                        },
                                                                        computed: False,
                                                                        value: {
                                                                            type: "Identifier",
                                                                            name: "icon"
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
                                                                                                value: "is_base_block",
                                                                                                raw: "\"is_base_block\""
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
                                                                                                    name: "BOOLEAN"
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
                                                                                                type: "CallExpression",
                                                                                                callee: {
                                                                                                    type: "MemberExpression",
                                                                                                    computed: False,
                                                                                                    object: {
                                                                                                        type: "Identifier",
                                                                                                        name: "Scratch"
                                                                                                    },
                                                                                                    property: {
                                                                                                        type: "Identifier",
                                                                                                        name: "translate"
                                                                                                    }
                                                                                                },
                                                                                                arguments: [
                                                                                                    {
                                                                                                        type: "ObjectExpression",
                                                                                                        properties: [
                                                                                                            {
                                                                                                                type: "Property",
                                                                                                                key: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "default"
                                                                                                                },
                                                                                                                computed: False,
                                                                                                                value: {
                                                                                                                    type: "Literal",
                                                                                                                    value: "is base [B] [A]?",
                                                                                                                    raw: "\"is base [B] [A]?\""
                                                                                                                },
                                                                                                                kind: "init",
                                                                                                                method: False,
                                                                                                                shorthand: False
                                                                                                            },
                                                                                                            {
                                                                                                                type: "Property",
                                                                                                                key: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "description"
                                                                                                                },
                                                                                                                computed: False,
                                                                                                                value: {
                                                                                                                    type: "Literal",
                                                                                                                    value: "[B] will be the base like 'base 10', [A] is the text we want to check if it is in that base",
                                                                                                                    raw: "\"[B] will be the base like 'base 10', [A] is the text we want to check if it is in that base\""
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
                                                                                                            name: "A"
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
                                                                                                                        value: "10",
                                                                                                                        raw: "\"10\""
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
                                                                                                            name: "B"
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
                                                                                                                        value: "base_menu",
                                                                                                                        raw: "\"base_menu\""
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
                                                                                                                        value: "10",
                                                                                                                        raw: "\"10\""
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
                                                                                                value: "base_block",
                                                                                                raw: "\"base_block\""
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
                                                                                                type: "CallExpression",
                                                                                                callee: {
                                                                                                    type: "MemberExpression",
                                                                                                    computed: False,
                                                                                                    object: {
                                                                                                        type: "Identifier",
                                                                                                        name: "Scratch"
                                                                                                    },
                                                                                                    property: {
                                                                                                        type: "Identifier",
                                                                                                        name: "translate"
                                                                                                    }
                                                                                                },
                                                                                                arguments: [
                                                                                                    {
                                                                                                        type: "ObjectExpression",
                                                                                                        properties: [
                                                                                                            {
                                                                                                                type: "Property",
                                                                                                                key: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "default"
                                                                                                                },
                                                                                                                computed: False,
                                                                                                                value: {
                                                                                                                    type: "Literal",
                                                                                                                    value: "[A] from base [B] to base [C]",
                                                                                                                    raw: "\"[A] from base [B] to base [C]\""
                                                                                                                },
                                                                                                                kind: "init",
                                                                                                                method: False,
                                                                                                                shorthand: False
                                                                                                            },
                                                                                                            {
                                                                                                                type: "Property",
                                                                                                                key: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "description"
                                                                                                                },
                                                                                                                computed: False,
                                                                                                                value: {
                                                                                                                    type: "Literal",
                                                                                                                    value: "[A] is the original number, [B] is the base it is currently in, [C] is the base it will be converted to.",
                                                                                                                    raw: "\"[A] is the original number, [B] is the base it is currently in, [C] is the base it will be converted to.\""
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
                                                                                                            name: "A"
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
                                                                                                                        value: "10",
                                                                                                                        raw: "\"10\""
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
                                                                                                            name: "B"
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
                                                                                                                        value: "base_menu",
                                                                                                                        raw: "\"base_menu\""
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
                                                                                                                        value: "10",
                                                                                                                        raw: "\"10\""
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
                                                                                                            name: "C"
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
                                                                                                                        value: "base_menu",
                                                                                                                        raw: "\"base_menu\""
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
                                                                                        name: "base_menu"
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
                                                                                                    value: True,
                                                                                                    raw: "true"
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
                                                                                                    type: "Identifier",
                                                                                                    name: "bases"
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
                                                name: "is_base_block"
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
                                                                    name: "A"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "A"
                                                                },
                                                                kind: "init",
                                                                method: False,
                                                                shorthand: True
                                                            },
                                                            {
                                                                type: "Property",
                                                                key: {
                                                                    type: "Identifier",
                                                                    name: "B"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "B"
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
                                                            type: "IfStatement",
                                                            test: {
                                                                type: "CallExpression",
                                                                callee: {
                                                                    type: "MemberExpression",
                                                                    computed: False,
                                                                    object: {
                                                                        type: "Identifier",
                                                                        name: "bases"
                                                                    },
                                                                    property: {
                                                                        type: "Identifier",
                                                                        name: "includes"
                                                                    }
                                                                },
                                                                arguments: [
                                                                    {
                                                                        type: "CallExpression",
                                                                        callee: {
                                                                            type: "MemberExpression",
                                                                            computed: False,
                                                                            object: {
                                                                                type: "Identifier",
                                                                                name: "cast"
                                                                            },
                                                                            property: {
                                                                                type: "Identifier",
                                                                                name: "toString"
                                                                            }
                                                                        },
                                                                        arguments: [
                                                                            {
                                                                                type: "Identifier",
                                                                                name: "B"
                                                                            }
                                                                        ]
                                                                    }
                                                                ]
                                                            },
                                                            consequent: {
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
                                                                                    type: "NewExpression",
                                                                                    callee: {
                                                                                        type: "Identifier",
                                                                                        name: "RegExp"
                                                                                    },
                                                                                    arguments: [
                                                                                        {
                                                                                            type: "BinaryExpression",
                                                                                            operator: "+",
                                                                                            left: {
                                                                                                type: "BinaryExpression",
                                                                                                operator: "+",
                                                                                                left: {
                                                                                                    type: "Literal",
                                                                                                    value: "^[",
                                                                                                    raw: "\"^[\""
                                                                                                },
                                                                                                right: {
                                                                                                    type: "CallExpression",
                                                                                                    callee: {
                                                                                                        type: "MemberExpression",
                                                                                                        computed: False,
                                                                                                        object: {
                                                                                                            type: "Identifier",
                                                                                                            name: "chars"
                                                                                                        },
                                                                                                        property: {
                                                                                                            type: "Identifier",
                                                                                                            name: "substring"
                                                                                                        }
                                                                                                    },
                                                                                                    arguments: [
                                                                                                        {
                                                                                                            type: "Literal",
                                                                                                            value: 0,
                                                                                                            raw: "0"
                                                                                                        },
                                                                                                        {
                                                                                                            type: "CallExpression",
                                                                                                            callee: {
                                                                                                                type: "MemberExpression",
                                                                                                                computed: False,
                                                                                                                object: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "cast"
                                                                                                                },
                                                                                                                property: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "toNumber"
                                                                                                                }
                                                                                                            },
                                                                                                            arguments: [
                                                                                                                {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "B"
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            },
                                                                                            right: {
                                                                                                type: "Literal",
                                                                                                value: "]+$",
                                                                                                raw: "\"]+$\""
                                                                                            }
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                property: {
                                                                                    type: "Identifier",
                                                                                    name: "test"
                                                                                }
                                                                            },
                                                                            arguments: [
                                                                                {
                                                                                    type: "CallExpression",
                                                                                    callee: {
                                                                                        type: "MemberExpression",
                                                                                        computed: False,
                                                                                        object: {
                                                                                            type: "Identifier",
                                                                                            name: "cast"
                                                                                        },
                                                                                        property: {
                                                                                            type: "Identifier",
                                                                                            name: "toString"
                                                                                        }
                                                                                    },
                                                                                    arguments: [
                                                                                        {
                                                                                            type: "Identifier",
                                                                                            name: "A"
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            type: "ReturnStatement",
                                                            argument: {
                                                                type: "Literal",
                                                                value: False,
                                                                raw: "false"
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
                                                name: "base_block"
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
                                                                    name: "A"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "A"
                                                                },
                                                                kind: "init",
                                                                method: False,
                                                                shorthand: True
                                                            },
                                                            {
                                                                type: "Property",
                                                                key: {
                                                                    type: "Identifier",
                                                                    name: "B"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "B"
                                                                },
                                                                kind: "init",
                                                                method: False,
                                                                shorthand: True
                                                            },
                                                            {
                                                                type: "Property",
                                                                key: {
                                                                    type: "Identifier",
                                                                    name: "C"
                                                                },
                                                                computed: False,
                                                                value: {
                                                                    type: "Identifier",
                                                                    name: "C"
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
                                                            type: "IfStatement",
                                                            test: {
                                                                type: "LogicalExpression",
                                                                operator: "&&",
                                                                left: {
                                                                    type: "CallExpression",
                                                                    callee: {
                                                                        type: "MemberExpression",
                                                                        computed: False,
                                                                        object: {
                                                                            type: "Identifier",
                                                                            name: "bases"
                                                                        },
                                                                        property: {
                                                                            type: "Identifier",
                                                                            name: "includes"
                                                                        }
                                                                    },
                                                                    arguments: [
                                                                        {
                                                                            type: "CallExpression",
                                                                            callee: {
                                                                                type: "MemberExpression",
                                                                                computed: False,
                                                                                object: {
                                                                                    type: "Identifier",
                                                                                    name: "cast"
                                                                                },
                                                                                property: {
                                                                                    type: "Identifier",
                                                                                    name: "toString"
                                                                                }
                                                                            },
                                                                            arguments: [
                                                                                {
                                                                                    type: "Identifier",
                                                                                    name: "B"
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                right: {
                                                                    type: "CallExpression",
                                                                    callee: {
                                                                        type: "MemberExpression",
                                                                        computed: False,
                                                                        object: {
                                                                            type: "Identifier",
                                                                            name: "bases"
                                                                        },
                                                                        property: {
                                                                            type: "Identifier",
                                                                            name: "includes"
                                                                        }
                                                                    },
                                                                    arguments: [
                                                                        {
                                                                            type: "CallExpression",
                                                                            callee: {
                                                                                type: "MemberExpression",
                                                                                computed: False,
                                                                                object: {
                                                                                    type: "Identifier",
                                                                                    name: "cast"
                                                                                },
                                                                                property: {
                                                                                    type: "Identifier",
                                                                                    name: "toString"
                                                                                }
                                                                            },
                                                                            arguments: [
                                                                                {
                                                                                    type: "Identifier",
                                                                                    name: "C"
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            consequent: {
                                                                type: "BlockStatement",
                                                                body: [
                                                                    {
                                                                        type: "IfStatement",
                                                                        test: {
                                                                            type: "CallExpression",
                                                                            callee: {
                                                                                type: "MemberExpression",
                                                                                computed: False,
                                                                                object: {
                                                                                    type: "NewExpression",
                                                                                    callee: {
                                                                                        type: "Identifier",
                                                                                        name: "RegExp"
                                                                                    },
                                                                                    arguments: [
                                                                                        {
                                                                                            type: "BinaryExpression",
                                                                                            operator: "+",
                                                                                            left: {
                                                                                                type: "BinaryExpression",
                                                                                                operator: "+",
                                                                                                left: {
                                                                                                    type: "Literal",
                                                                                                    value: "^[",
                                                                                                    raw: "\"^[\""
                                                                                                },
                                                                                                right: {
                                                                                                    type: "CallExpression",
                                                                                                    callee: {
                                                                                                        type: "MemberExpression",
                                                                                                        computed: False,
                                                                                                        object: {
                                                                                                            type: "Identifier",
                                                                                                            name: "chars"
                                                                                                        },
                                                                                                        property: {
                                                                                                            type: "Identifier",
                                                                                                            name: "substring"
                                                                                                        }
                                                                                                    },
                                                                                                    arguments: [
                                                                                                        {
                                                                                                            type: "Literal",
                                                                                                            value: 0,
                                                                                                            raw: "0"
                                                                                                        },
                                                                                                        {
                                                                                                            type: "CallExpression",
                                                                                                            callee: {
                                                                                                                type: "MemberExpression",
                                                                                                                computed: False,
                                                                                                                object: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "cast"
                                                                                                                },
                                                                                                                property: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "toNumber"
                                                                                                                }
                                                                                                            },
                                                                                                            arguments: [
                                                                                                                {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "B"
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            },
                                                                                            right: {
                                                                                                type: "Literal",
                                                                                                value: "]+$",
                                                                                                raw: "\"]+$\""
                                                                                            }
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                property: {
                                                                                    type: "Identifier",
                                                                                    name: "test"
                                                                                }
                                                                            },
                                                                            arguments: [
                                                                                {
                                                                                    type: "CallExpression",
                                                                                    callee: {
                                                                                        type: "MemberExpression",
                                                                                        computed: False,
                                                                                        object: {
                                                                                            type: "Identifier",
                                                                                            name: "cast"
                                                                                        },
                                                                                        property: {
                                                                                            type: "Identifier",
                                                                                            name: "toString"
                                                                                        }
                                                                                    },
                                                                                    arguments: [
                                                                                        {
                                                                                            type: "Identifier",
                                                                                            name: "A"
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        },
                                                                        consequent: {
                                                                            type: "BlockStatement",
                                                                            body: [
                                                                                {
                                                                                    type: "ReturnStatement",
                                                                                    argument: {
                                                                                        type: "LogicalExpression",
                                                                                        operator: "||",
                                                                                        left: {
                                                                                            type: "CallExpression",
                                                                                            callee: {
                                                                                                type: "MemberExpression",
                                                                                                computed: False,
                                                                                                object: {
                                                                                                    type: "CallExpression",
                                                                                                    callee: {
                                                                                                        type: "MemberExpression",
                                                                                                        computed: False,
                                                                                                        object: {
                                                                                                            type: "CallExpression",
                                                                                                            callee: {
                                                                                                                type: "Identifier",
                                                                                                                name: "parseInt"
                                                                                                            },
                                                                                                            arguments: [
                                                                                                                {
                                                                                                                    type: "CallExpression",
                                                                                                                    callee: {
                                                                                                                        type: "MemberExpression",
                                                                                                                        computed: False,
                                                                                                                        object: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "cast"
                                                                                                                        },
                                                                                                                        property: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "toString"
                                                                                                                        }
                                                                                                                    },
                                                                                                                    arguments: [
                                                                                                                        {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "A"
                                                                                                                        }
                                                                                                                    ]
                                                                                                                },
                                                                                                                {
                                                                                                                    type: "CallExpression",
                                                                                                                    callee: {
                                                                                                                        type: "MemberExpression",
                                                                                                                        computed: False,
                                                                                                                        object: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "cast"
                                                                                                                        },
                                                                                                                        property: {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "toNumber"
                                                                                                                        }
                                                                                                                    },
                                                                                                                    arguments: [
                                                                                                                        {
                                                                                                                            type: "Identifier",
                                                                                                                            name: "B"
                                                                                                                        }
                                                                                                                    ]
                                                                                                                }
                                                                                                            ]
                                                                                                        },
                                                                                                        property: {
                                                                                                            type: "Identifier",
                                                                                                            name: "toString"
                                                                                                        }
                                                                                                    },
                                                                                                    arguments: [
                                                                                                        {
                                                                                                            type: "CallExpression",
                                                                                                            callee: {
                                                                                                                type: "MemberExpression",
                                                                                                                computed: False,
                                                                                                                object: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "cast"
                                                                                                                },
                                                                                                                property: {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "toNumber"
                                                                                                                }
                                                                                                            },
                                                                                                            arguments: [
                                                                                                                {
                                                                                                                    type: "Identifier",
                                                                                                                    name: "C"
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    ]
                                                                                                },
                                                                                                property: {
                                                                                                    type: "Identifier",
                                                                                                    name: "toUpperCase"
                                                                                                }
                                                                                            },
                                                                                            arguments: []
                                                                                        },
                                                                                        right: {
                                                                                            type: "Literal",
                                                                                            value: "0",
                                                                                            raw: "\"0\""
                                                                                        }
                                                                                    }
                                                                                }
                                                                            ]
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            type: "ReturnStatement",
                                                            argument: {
                                                                type: "Literal",
                                                                value: "0",
                                                                raw: "\"0\""
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
                                                name: "ScratchBase"
                                            },
                                            arguments: []
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