program:
  class_declaration:
    class ('class')
    identifier ('AsyncExtension')
    class_body:
      { ('{')
      method_definition:
        property_identifier ('getInfo')
        formal_parameters:
          ( ('(')
          ) (')')
        statement_block:
          { ('{')
          return_statement:
            return ('return')
            object:
              { ('{')
              pair:
                property_identifier ('id')
                : (':')
                string:
                  ' ("'")
                  string_fragment ('asyncexample')
                  ' ("'")
              , (',')
              pair:
                property_identifier ('name')
                : (':')
                string:
                  ' ("'")
                  string_fragment ('Async Blocks')
                  ' ("'")
              , (',')
              pair:
                property_identifier ('blocks')
                : (':')
                array:
                  [ ('[')
                  object:
                    { ('{')
                    pair:
                      property_identifier ('opcode')
                      : (':')
                      string:
                        ' ("'")
                        string_fragment ('wait')
                        ' ("'")
                    , (',')
                    pair:
                      property_identifier ('text')
                      : (':')
                      string:
                        ' ("'")
                        string_fragment ('wait [TIME] seconds')
                        ' ("'")
                    , (',')
                    pair:
                      property_identifier ('blockType')
                      : (':')
                      member_expression:
                        member_expression:
                          identifier ('Scratch')
                          . ('.')
                          property_identifier ('BlockType')
                        . ('.')
                        property_identifier ('COMMAND')
                    , (',')
                    pair:
                      property_identifier ('arguments')
                      : (':')
                      object:
                        { ('{')
                        pair:
                          property_identifier ('TIME')
                          : (':')
                          object:
                            { ('{')
                            pair:
                              property_identifier ('type')
                              : (':')
                              member_expression:
                                member_expression:
                                  identifier ('Scratch')
                                  . ('.')
                                  property_identifier ('ArgumentType')
                                . ('.')
                                property_identifier ('NUMBER')
                            , (',')
                            pair:
                              property_identifier ('defaultValue')
                              : (':')
                              number ('1')
                            } ('}')
                        } ('}')
                    } ('}')
                  , (',')
                  object:
                    { ('{')
                    pair:
                      property_identifier ('opcode')
                      : (':')
                      string:
                        ' ("'")
                        string_fragment ('fetch')
                        ' ("'")
                    , (',')
                    pair:
                      property_identifier ('text')
                      : (':')
                      string:
                        ' ("'")
                        string_fragment ('fetch [URL]')
                        ' ("'")
                    , (',')
                    pair:
                      property_identifier ('blockType')
                      : (':')
                      member_expression:
                        member_expression:
                          identifier ('Scratch')
                          . ('.')
                          property_identifier ('BlockType')
                        . ('.')
                        property_identifier ('REPORTER')
                    , (',')
                    pair:
                      property_identifier ('arguments')
                      : (':')
                      object:
                        { ('{')
                        pair:
                          property_identifier ('URL')
                          : (':')
                          object:
                            { ('{')
                            pair:
                              property_identifier ('type')
                              : (':')
                              member_expression:
                                member_expression:
                                  identifier ('Scratch')
                                  . ('.')
                                  property_identifier ('ArgumentType')
                                . ('.')
                                property_identifier ('STRING')
                            , (',')
                            pair:
                              property_identifier ('defaultValue')
                              : (':')
                              string:
                                ' ("'")
                                string_fragment ('https://extensions.turbowarp.org/hello.txt')
                                ' ("'")
                            } ('}')
                        } ('}')
                    } ('}')
                  ] (']')
              } ('}')
            ; (';')
          } ('}')
      method_definition:
        property_identifier ('wait')
        formal_parameters:
          ( ('(')
          identifier ('args')
          ) (')')
        statement_block:
          { ('{')
          return_statement:
            return ('return')
            new_expression:
              new ('new')
              identifier ('Promise')
              arguments:
                ( ('(')
                arrow_function:
                  formal_parameters:
                    ( ('(')
                    identifier ('resolve')
                    , (',')
                    identifier ('reject')
                    ) (')')
                  => ('=>')
                  statement_block:
                    { ('{')
                    lexical_declaration:
                      const ('const')
                      variable_declarator:
                        identifier ('timeInMilliseconds')
                        = ('=')
                        binary_expression:
                          member_expression:
                            identifier ('args')
                            . ('.')
                            property_identifier ('TIME')
                          * ('*')
                          number ('1000')
                      ; (';')
                    expression_statement:
                      call_expression:
                        identifier ('setTimeout')
                        arguments:
                          ( ('(')
                          arrow_function:
                            formal_parameters:
                              ( ('(')
                              ) (')')
                            => ('=>')
                            statement_block:
                              { ('{')
                              expression_statement:
                                call_expression:
                                  identifier ('resolve')
                                  arguments:
                                    ( ('(')
                                    ) (')')
                                ; (';')
                              } ('}')
                          , (',')
                          identifier ('timeInMilliseconds')
                          ) (')')
                      ; (';')
                    } ('}')
                ) (')')
            ; (';')
          } ('}')
      method_definition:
        property_identifier ('fetch')
        formal_parameters:
          ( ('(')
          identifier ('args')
          ) (')')
        statement_block:
          { ('{')
          return_statement:
            return ('return')
            call_expression:
              member_expression:
                call_expression:
                  member_expression:
                    call_expression:
                      identifier ('fetch')
                      arguments:
                        ( ('(')
                        member_expression:
                          identifier ('args')
                          . ('.')
                          property_identifier ('URL')
                        ) (')')
                    . ('.')
                    property_identifier ('then')
                  arguments:
                    ( ('(')
                    arrow_function:
                      formal_parameters:
                        ( ('(')
                        identifier ('response')
                        ) (')')
                      => ('=>')
                      statement_block:
                        { ('{')
                        return_statement:
                          return ('return')
                          call_expression:
                            member_expression:
                              identifier ('response')
                              . ('.')
                              property_identifier ('text')
                            arguments:
                              ( ('(')
                              ) (')')
                          ; (';')
                        } ('}')
                    ) (')')
                . ('.')
                property_identifier ('catch')
              arguments:
                ( ('(')
                arrow_function:
                  formal_parameters:
                    ( ('(')
                    identifier ('error')
                    ) (')')
                  => ('=>')
                  statement_block:
                    { ('{')
                    expression_statement:
                      call_expression:
                        member_expression:
                          identifier ('console')
                          . ('.')
                          property_identifier ('error')
                        arguments:
                          ( ('(')
                          identifier ('error')
                          ) (')')
                      ; (';')
                    return_statement:
                      return ('return')
                      string:
                        ' ("'")
                        string_fragment ('Uh oh! Something went wrong.')
                        ' ("'")
                      ; (';')
                    } ('}')
                ) (')')
            ; (';')
          } ('}')
      } ('}')
  expression_statement:
    call_expression:
      member_expression:
        member_expression:
          identifier ('Scratch')
          . ('.')
          property_identifier ('extensions')
        . ('.')
        property_identifier ('register')
      arguments:
        ( ('(')
        new_expression:
          new ('new')
          identifier ('AsyncExtension')
          arguments:
            ( ('(')
            ) (')')
        ) (')')
    ; (';')