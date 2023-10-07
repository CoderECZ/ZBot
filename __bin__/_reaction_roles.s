  0           0 RESUME                   0

  1           2 LOAD_CONST               0 (0)
              4 LOAD_CONST               1 (None)
              6 IMPORT_NAME              0 (discord)
              8 STORE_NAME               0 (discord)

  2          10 LOAD_CONST               0 (0)
             12 LOAD_CONST               2 (('commands',))
             14 IMPORT_NAME              1 (discord.ext)
             16 IMPORT_FROM              2 (commands)
             18 STORE_NAME               2 (commands)
             20 POP_TOP

  4          22 LOAD_CONST               0 (0)
             24 LOAD_CONST               3 (('Logging',))
             26 IMPORT_NAME              3 (cogs.logging)
             28 IMPORT_FROM              4 (Logging)
             30 STORE_NAME               4 (Logging)
             32 POP_TOP

  6          34 PUSH_NULL
             36 LOAD_BUILD_CLASS
             38 LOAD_CONST               4 (<code object ReactionRoles at 0x564d34183b80, file "example.py", line 6>)
             40 MAKE_FUNCTION            0
             42 LOAD_CONST               5 ('ReactionRoles')
             44 LOAD_NAME                2 (commands)
             46 LOAD_ATTR                5 (Cog)
             56 PRECALL                  3
             60 CALL                     3
             70 STORE_NAME               6 (ReactionRoles)
             72 LOAD_CONST               1 (None)
             74 RETURN_VALUE

Disassembly of <code object ReactionRoles at 0x564d34183b80, file "example.py", line 6>:
  6           0 RESUME                   0
              2 LOAD_NAME                0 (__name__)
              4 STORE_NAME               1 (__module__)
              6 LOAD_CONST               0 ('ReactionRoles')
              8 STORE_NAME               2 (__qualname__)

  7          10 LOAD_CONST               1 (<code object __init__ at 0x564d34173060, file "example.py", line 7>)
             12 MAKE_FUNCTION            0
             14 STORE_NAME               3 (__init__)

 38          16 PUSH_NULL
             18 LOAD_NAME                4 (commands)
             20 LOAD_ATTR                5 (command)
             30 LOAD_CONST               2 ('admin_roles')
             32 KW_NAMES                 3
             34 PRECALL                  1
             38 CALL                     1

 39          48 PUSH_NULL
             50 LOAD_NAME                4 (commands)
             52 LOAD_ATTR                6 (has_permissions)
             62 LOAD_CONST               4 (True)
             64 KW_NAMES                 5
             66 PRECALL                  1
             70 CALL                     1

 40          80 LOAD_CONST               6 (<code object admin_roles at 0x564d34118a60, file "example.py", line 38>)
             82 MAKE_FUNCTION            0

 39          84 PRECALL                  0
             88 CALL                     0

 38          98 PRECALL                  0
            102 CALL                     0

 40         112 STORE_NAME               7 (admin_roles)

 66         114 LOAD_NAME                4 (commands)
            116 LOAD_ATTR                8 (Cog)
            126 LOAD_METHOD              9 (listener)
            148 PRECALL                  0
            152 CALL                     0

 67         162 LOAD_CONST               7 ('reaction')
            164 LOAD_NAME               10 (discord)
            166 LOAD_ATTR               11 (Reaction)
            176 LOAD_CONST               8 ('user')
            178 LOAD_NAME               10 (discord)
            180 LOAD_ATTR               12 (Member)
            190 BUILD_TUPLE              4
            192 LOAD_CONST               9 (<code object on_reaction_add at 0x564d3418db70, file "example.py", line 66>)
            194 MAKE_FUNCTION            4 (annotations)

 66         196 PRECALL                  0
            200 CALL                     0

 67         210 STORE_NAME              13 (on_reaction_add)

 92         212 LOAD_NAME                4 (commands)
            214 LOAD_ATTR                8 (Cog)
            224 LOAD_METHOD              9 (listener)
            246 PRECALL                  0
            250 CALL                     0

 93         260 LOAD_CONST               7 ('reaction')
            262 LOAD_NAME               10 (discord)
            264 LOAD_ATTR               11 (Reaction)
            274 LOAD_CONST               8 ('user')
            276 LOAD_NAME               10 (discord)
            278 LOAD_ATTR               12 (Member)
            288 BUILD_TUPLE              4
            290 LOAD_CONST              10 (<code object on_reaction_remove at 0x564d3418c370, file "example.py", line 92>)
            292 MAKE_FUNCTION            4 (annotations)

 92         294 PRECALL                  0
            298 CALL                     0

 93         308 STORE_NAME              14 (on_reaction_remove)
            310 LOAD_CONST              11 (None)
            312 RETURN_VALUE

Disassembly of <code object __init__ at 0x564d34173060, file "example.py", line 7>:
  7           0 RESUME                   0

  8           2 LOAD_CONST               1 (1088951646886842498)
              4 LOAD_FAST                0 (self)
              6 STORE_ATTR               0 (server_id)

  9          16 LOAD_FAST                1 (bot)
             18 LOAD_METHOD              1 (get_guild)
             40 LOAD_FAST                0 (self)
             42 LOAD_ATTR                0 (server_id)
             52 PRECALL                  1
             56 CALL                     1
             66 LOAD_FAST                0 (self)
             68 STORE_ATTR               2 (server)

 12          78 BUILD_MAP                0

 13          80 LOAD_CONST               2 ('<:Swift:1159231251748769943>')
             82 LOAD_GLOBAL              6 (discord)
             94 LOAD_ATTR                4 (utils)
            104 LOAD_METHOD              5 (get)
            126 LOAD_FAST                0 (self)
            128 LOAD_ATTR                2 (server)
            138 LOAD_ATTR                6 (roles)
            148 LOAD_CONST               3 ('Swift')
            150 KW_NAMES                 4
            152 PRECALL                  2
            156 CALL                     2

 12         166 MAP_ADD                  1

 14         168 LOAD_CONST               5 ('<:PHP:1159231250201063454>')
            170 LOAD_GLOBAL              6 (discord)
            182 LOAD_ATTR                4 (utils)
            192 LOAD_METHOD              5 (get)
            214 LOAD_FAST                0 (self)
            216 LOAD_ATTR                2 (server)
            226 LOAD_ATTR                6 (roles)
            236 LOAD_CONST               6 ('PHP')
            238 KW_NAMES                 4
            240 PRECALL                  2
            244 CALL                     2

 12         254 MAP_ADD                  1

 15         256 LOAD_CONST               7 ('<:Net:1159231247663513692>')
            258 LOAD_GLOBAL              6 (discord)
            270 LOAD_ATTR                4 (utils)
            280 LOAD_METHOD              5 (get)
            302 LOAD_FAST                0 (self)
            304 LOAD_ATTR                2 (server)
            314 LOAD_ATTR                6 (roles)
            324 LOAD_CONST               8 ('.NET')
            326 KW_NAMES                 4
            328 PRECALL                  2
            332 CALL                     2

 12         342 MAP_ADD                  1

 16         344 LOAD_CONST               9 ('<:Golang:1159231246371651686>')
            346 LOAD_GLOBAL              6 (discord)
            358 LOAD_ATTR                4 (utils)
            368 LOAD_METHOD              5 (get)
            390 LOAD_FAST                0 (self)
            392 LOAD_ATTR                2 (server)
            402 LOAD_ATTR                6 (roles)
            412 LOAD_CONST              10 ('Golang')
            414 KW_NAMES                 4
            416 PRECALL                  2
            420 CALL                     2

 12         430 MAP_ADD                  1

 17         432 LOAD_CONST              11 ('<:Java:1159231242768748587>')
            434 LOAD_GLOBAL              6 (discord)
            446 LOAD_ATTR                4 (utils)
            456 LOAD_METHOD              5 (get)
            478 LOAD_FAST                0 (self)
            480 LOAD_ATTR                2 (server)
            490 LOAD_ATTR                6 (roles)
            500 LOAD_CONST              12 ('Java')
            502 KW_NAMES                 4
            504 PRECALL                  2
            508 CALL                     2

 12         518 MAP_ADD                  1

 18         520 LOAD_CONST              13 ('<:Clang:1159231240654819408>')
            522 LOAD_GLOBAL              6 (discord)
            534 LOAD_ATTR                4 (utils)
            544 LOAD_METHOD              5 (get)
            566 LOAD_FAST                0 (self)
            568 LOAD_ATTR                2 (server)
            578 LOAD_ATTR                6 (roles)
            588 LOAD_CONST              14 ('Clang')
            590 KW_NAMES                 4
            592 PRECALL                  2
            596 CALL                     2

 12         606 MAP_ADD                  1

 19         608 LOAD_CONST              15 ('<:Blender:1159231237676863569>')
            610 LOAD_GLOBAL              6 (discord)
            622 LOAD_ATTR                4 (utils)
            632 LOAD_METHOD              5 (get)
            654 LOAD_FAST                0 (self)
            656 LOAD_ATTR                2 (server)
            666 LOAD_ATTR                6 (roles)
            676 LOAD_CONST              16 ('Blender')
            678 KW_NAMES                 4
            680 PRECALL                  2
            684 CALL                     2

 12         694 MAP_ADD                  1

 20         696 LOAD_CONST              17 ('<:VisualStudio:1159231208916521000>')
            698 LOAD_GLOBAL              6 (discord)
            710 LOAD_ATTR                4 (utils)
            720 LOAD_METHOD              5 (get)
            742 LOAD_FAST                0 (self)
            744 LOAD_ATTR                2 (server)
            754 LOAD_ATTR                6 (roles)
            764 LOAD_CONST              18 ('Visual Studio')
            766 KW_NAMES                 4
            768 PRECALL                  2
            772 CALL                     2

 12         782 MAP_ADD                  1

 21         784 LOAD_CONST              19 ('<:JavaScript:1159231203124183151>')
            786 LOAD_GLOBAL              6 (discord)
            798 LOAD_ATTR                4 (utils)
            808 LOAD_METHOD              5 (get)
            830 LOAD_FAST                0 (self)
            832 LOAD_ATTR                2 (server)
            842 LOAD_ATTR                6 (roles)
            852 LOAD_CONST              20 ('JavaScript')
            854 KW_NAMES                 4
            856 PRECALL                  2
            860 CALL                     2

 12         870 MAP_ADD                  1

 22         872 LOAD_CONST              21 ('<:Python:1159231201765240892>')
            874 LOAD_GLOBAL              6 (discord)
            886 LOAD_ATTR                4 (utils)
            896 LOAD_METHOD              5 (get)
            918 LOAD_FAST                0 (self)
            920 LOAD_ATTR                2 (server)
            930 LOAD_ATTR                6 (roles)
            940 LOAD_CONST              22 ('Python')
            942 KW_NAMES                 4
            944 PRECALL                  2
            948 CALL                     2

 12         958 MAP_ADD                  1

 23         960 LOAD_CONST              23 ('<:HTML:1159231198774702091>')
            962 LOAD_GLOBAL              6 (discord)
            974 LOAD_ATTR                4 (utils)
            984 LOAD_METHOD              5 (get)
           1006 LOAD_FAST                0 (self)
           1008 LOAD_ATTR                2 (server)
           1018 LOAD_ATTR                6 (roles)
           1028 LOAD_CONST              24 ('HTML')
           1030 KW_NAMES                 4
           1032 PRECALL                  2
           1036 CALL                     2

 12        1046 MAP_ADD                  1

 24        1048 LOAD_CONST              25 ('<:CPP:1159231197059227809>')
           1050 LOAD_GLOBAL              6 (discord)
           1062 LOAD_ATTR                4 (utils)
           1072 LOAD_METHOD              5 (get)
           1094 LOAD_FAST                0 (self)
           1096 LOAD_ATTR                2 (server)
           1106 LOAD_ATTR                6 (roles)
           1116 LOAD_CONST              26 ('CPP')
           1118 KW_NAMES                 4
           1120 PRECALL                  2
           1124 CALL                     2

 12        1134 MAP_ADD                  1

 25        1136 LOAD_CONST              27 ('<:CS:1159231195712847962>')
           1138 LOAD_GLOBAL              6 (discord)
           1150 LOAD_ATTR                4 (utils)
           1160 LOAD_METHOD              5 (get)
           1182 LOAD_FAST                0 (self)
           1184 LOAD_ATTR                2 (server)
           1194 LOAD_ATTR                6 (roles)
           1204 LOAD_CONST              28 ('CS')
           1206 KW_NAMES                 4
           1208 PRECALL                  2
           1212 CALL                     2

 12        1222 MAP_ADD                  1

 26        1224 LOAD_CONST              29 ('<:VSC:1159231193359863898>')
           1226 LOAD_GLOBAL              6 (discord)
           1238 LOAD_ATTR                4 (utils)
           1248 LOAD_METHOD              5 (get)
           1270 LOAD_FAST                0 (self)
           1272 LOAD_ATTR                2 (server)
           1282 LOAD_ATTR                6 (roles)
           1292 LOAD_CONST              30 ('Visual Studio Code')
           1294 KW_NAMES                 4
           1296 PRECALL                  2
           1300 CALL                     2

 12        1310 MAP_ADD                  1

 27        1312 LOAD_CONST              31 ('<:CSS:1159231142633943203>')
           1314 LOAD_GLOBAL              6 (discord)
           1326 LOAD_ATTR                4 (utils)
           1336 LOAD_METHOD              5 (get)
           1358 LOAD_FAST                0 (self)
           1360 LOAD_ATTR                2 (server)
           1370 LOAD_ATTR                6 (roles)
           1380 LOAD_CONST              32 ('CSS')
           1382 KW_NAMES                 4
           1384 PRECALL                  2
           1388 CALL                     2

 12        1398 MAP_ADD                  1

 28        1400 LOAD_CONST              33 ('<:Lua:1159231140377411624>')
           1402 LOAD_GLOBAL              6 (discord)
           1414 LOAD_ATTR                4 (utils)
           1424 LOAD_METHOD              5 (get)
           1446 LOAD_FAST                0 (self)
           1448 LOAD_ATTR                2 (server)
           1458 LOAD_ATTR                6 (roles)
           1468 LOAD_CONST              34 ('Lua')
           1470 KW_NAMES                 4
           1472 PRECALL                  2
           1476 CALL                     2

 12        1486 MAP_ADD                  1

 29        1488 LOAD_CONST              35 ('<:SQL:1159231136392818718>')
           1490 LOAD_GLOBAL              6 (discord)
           1502 LOAD_ATTR                4 (utils)
           1512 LOAD_METHOD              5 (get)
           1534 LOAD_FAST                0 (self)
           1536 LOAD_ATTR                2 (server)
           1546 LOAD_ATTR                6 (roles)
           1556 LOAD_CONST              36 ('SQL')
           1558 KW_NAMES                 4
           1560 PRECALL                  2
           1564 CALL                     2

 12        1574 MAP_ADD                  1

 30        1576 LOAD_CONST              37 ('<:GitHub:1159249963331637401>')
           1578 LOAD_GLOBAL              6 (discord)
           1590 LOAD_ATTR                4 (utils)
           1600 LOAD_METHOD              5 (get)
           1622 LOAD_FAST                0 (self)
           1624 LOAD_ATTR                2 (server)
           1634 LOAD_ATTR                6 (roles)
           1644 LOAD_CONST              38 ('Git/GitHub')
           1646 KW_NAMES                 4
           1648 PRECALL                  2
           1652 CALL                     2

 12        1662 BUILD_MAP                1
           1664 DICT_UPDATE              1
           1666 STORE_FAST               2 (reactionRoles)

 33        1668 LOAD_FAST                1 (bot)
           1670 LOAD_FAST                0 (self)
           1672 STORE_ATTR               7 (bot)

 34        1682 LOAD_FAST                2 (reactionRoles)
           1684 LOAD_FAST                0 (self)
           1686 STORE_ATTR               8 (reactions)

 35        1696 LOAD_FAST                0 (self)
           1698 LOAD_ATTR                8 (reactions)
           1708 LOAD_METHOD              9 (keys)
           1730 PRECALL                  0
           1734 CALL                     0
           1744 LOAD_FAST                0 (self)
           1746 STORE_ATTR              10 (reactionKeys)

 36        1756 LOAD_CONST               0 (None)
           1758 LOAD_FAST                0 (self)
           1760 STORE_ATTR              11 (message)
           1770 LOAD_CONST               0 (None)
           1772 RETURN_VALUE

Disassembly of <code object admin_roles at 0x564d34118a60, file "example.py", line 38>:
 38           0 RETURN_GENERATOR
              2 POP_TOP
              4 RESUME                   0

 41           6 LOAD_GLOBAL              1 (NULL + discord)
             18 LOAD_ATTR                1 (Embed)

 42          28 LOAD_CONST               1 ('Coding Roles')

 43          30 LOAD_CONST               2 ('Please react for the roles you wish to obtain below.\n\n')

 44          32 LOAD_CONST               3 (2003199)

 41          34 KW_NAMES                 4
             36 PRECALL                  3
             40 CALL                     3
             50 STORE_FAST               2 (embedLanguages)

 47          52 LOAD_FAST                0 (self)
             54 LOAD_ATTR                2 (reactionKeys)
             64 GET_ITER
        >>   66 FOR_ITER                59 (to 186)
             68 STORE_FAST               3 (key)

 48          70 LOAD_FAST                3 (key)
             72 STORE_FAST               4 (emoji)

 49          74 LOAD_FAST                3 (key)
             76 LOAD_METHOD              3 (split)
             98 LOAD_CONST               5 (':')
            100 PRECALL                  1
            104 CALL                     1
            114 LOAD_CONST               6 (1)
            116 BINARY_SUBSCR
            126 STORE_FAST               5 (nameKey)

 52         128 LOAD_FAST                2 (embedLanguages)
            130 LOAD_METHOD              4 (add_field)
            152 LOAD_FAST                4 (emoji)
            154 FORMAT_VALUE             0
            156 LOAD_CONST               7 (' - ')
            158 LOAD_FAST                5 (nameKey)
            160 FORMAT_VALUE             0
            162 BUILD_STRING             3
            164 LOAD_CONST               8 ('')
            166 KW_NAMES                 9
            168 PRECALL                  2
            172 CALL                     2
            182 POP_TOP
            184 JUMP_BACKWARD           60 (to 66)

 54     >>  186 LOAD_FAST                2 (embedLanguages)
            188 LOAD_METHOD              5 (set_footer)

 55         210 LOAD_CONST              10 ('https://cdn.discordapp.com/attachments/1114686704658423848/1157276152642146365/Picsart_23-09-17_19-07-53-355-removebg-preview.png?ex=651df3a7&is=651ca227&hm=ba913fbfa95aded5a1ef249cd7795d77e9f2087629b8dc9d3656736f065b6932&')

 56         212 LOAD_CONST              11 ('CoderZ')

 54         214 KW_NAMES                12
            216 PRECALL                  2
            220 CALL                     2
            230 POP_TOP

 58         232 LOAD_FAST                1 (ctx)
            234 LOAD_METHOD              6 (send)
            256 LOAD_FAST                2 (embedLanguages)
            258 KW_NAMES                13
            260 PRECALL                  1
            264 CALL                     1
            274 GET_AWAITABLE            0
            276 LOAD_CONST               0 (None)
        >>  278 SEND                     3 (to 286)
            280 YIELD_VALUE
            282 RESUME                   3
            284 JUMP_BACKWARD_NO_INTERRUPT     4 (to 278)
        >>  286 LOAD_FAST                0 (self)
            288 STORE_ATTR               7 (message)

 60         298 LOAD_FAST                0 (self)
            300 LOAD_ATTR                2 (reactionKeys)
            310 GET_ITER
        >>  312 FOR_ITER                93 (to 500)
            314 STORE_FAST               3 (key)

 61         316 NOP

 62         318 LOAD_FAST                0 (self)
            320 LOAD_ATTR                7 (message)
            330 LOAD_METHOD              8 (add_reaction)
            352 LOAD_FAST                3 (key)
            354 PRECALL                  1
            358 CALL                     1
            368 GET_AWAITABLE            0
            370 LOAD_CONST               0 (None)
        >>  372 SEND                     3 (to 380)
            374 YIELD_VALUE
            376 RESUME                   3
            378 JUMP_BACKWARD_NO_INTERRUPT     4 (to 372)
        >>  380 POP_TOP
            382 JUMP_BACKWARD           36 (to 312)
        >>  384 PUSH_EXC_INFO

 63         386 LOAD_GLOBAL              0 (discord)
            398 LOAD_ATTR                9 (HTTPException)
            408 CHECK_EXC_MATCH
            410 POP_JUMP_FORWARD_IF_FALSE    40 (to 492)
            412 STORE_FAST               6 (e)

 64         414 LOAD_FAST                1 (ctx)
            416 LOAD_METHOD              6 (send)
            438 LOAD_CONST              14 ('Could not add reactions: ')
            440 LOAD_FAST                6 (e)
            442 FORMAT_VALUE             0
            444 BUILD_STRING             2
            446 PRECALL                  1
            450 CALL                     1
            460 GET_AWAITABLE            0
            462 LOAD_CONST               0 (None)
        >>  464 SEND                     3 (to 472)
            466 YIELD_VALUE
            468 RESUME                   3
            470 JUMP_BACKWARD_NO_INTERRUPT     4 (to 464)
        >>  472 POP_TOP
            474 POP_EXCEPT
            476 LOAD_CONST               0 (None)
            478 STORE_FAST               6 (e)
            480 DELETE_FAST              6 (e)
            482 JUMP_BACKWARD           86 (to 312)
        >>  484 LOAD_CONST               0 (None)
            486 STORE_FAST               6 (e)
            488 DELETE_FAST              6 (e)
            490 RERAISE                  1

 63     >>  492 RERAISE                  0
        >>  494 COPY                     3
            496 POP_EXCEPT
            498 RERAISE                  1

 60     >>  500 LOAD_CONST               0 (None)
            502 RETURN_VALUE
ExceptionTable:
  318 to 380 -> 384 [1]
  384 to 412 -> 494 [2] lasti
  414 to 472 -> 484 [2] lasti
  484 to 492 -> 494 [2] lasti

Disassembly of <code object on_reaction_add at 0x564d3418db70, file "example.py", line 66>:
 66           0 RETURN_GENERATOR
              2 POP_TOP
              4 RESUME                   0

 68           6 LOAD_FAST                2 (user)
              8 LOAD_ATTR                0 (bot)
             18 POP_JUMP_FORWARD_IF_FALSE     2 (to 24)

 69          20 LOAD_CONST               0 (None)
             22 RETURN_VALUE

 71     >>   24 LOAD_GLOBAL              2 (discord)
             36 LOAD_ATTR                2 (utils)
             46 LOAD_METHOD              3 (get)
             68 LOAD_FAST                0 (self)
             70 LOAD_ATTR                4 (server)
             80 LOAD_ATTR                5 (roles)
             90 LOAD_CONST               1 ('---------------- Coding ----------------')
             92 KW_NAMES                 2
             94 PRECALL                  2
             98 CALL                     2
            108 STORE_FAST               3 (codeRole)

 73         110 LOAD_GLOBAL             13 (NULL + str)
            122 LOAD_FAST                1 (reaction)
            124 LOAD_ATTR                7 (emoji)
            134 PRECALL                  1
            138 CALL                     1
            148 LOAD_FAST                0 (self)
            150 LOAD_ATTR                8 (reactions)
            160 CONTAINS_OP              0
            162 POP_JUMP_FORWARD_IF_FALSE   221 (to 606)

 74         164 LOAD_FAST                0 (self)
            166 LOAD_ATTR                8 (reactions)
            176 LOAD_GLOBAL             13 (NULL + str)
            188 LOAD_FAST                1 (reaction)
            190 LOAD_ATTR                7 (emoji)
            200 PRECALL                  1
            204 CALL                     1
            214 BINARY_SUBSCR
            224 STORE_FAST               4 (role)

 76         226 NOP

 77         228 LOAD_FAST                4 (role)
            230 LOAD_FAST                2 (user)
            232 LOAD_ATTR                5 (roles)
            242 CONTAINS_OP              0
            244 POP_JUMP_FORWARD_IF_FALSE    29 (to 304)

 78         246 LOAD_FAST                2 (user)
            248 LOAD_METHOD              9 (remove_roles)
            270 LOAD_FAST                4 (role)
            272 PRECALL                  1
            276 CALL                     1
            286 GET_AWAITABLE            0
            288 LOAD_CONST               0 (None)
        >>  290 SEND                     3 (to 298)
            292 YIELD_VALUE
            294 RESUME                   3
            296 JUMP_BACKWARD_NO_INTERRUPT     4 (to 290)
        >>  298 POP_TOP
            300 LOAD_CONST               0 (None)
            302 RETURN_VALUE

 80     >>  304 LOAD_FAST                2 (user)
            306 LOAD_METHOD             10 (add_roles)
            328 LOAD_FAST                4 (role)
            330 PRECALL                  1
            334 CALL                     1
            344 GET_AWAITABLE            0
            346 LOAD_CONST               0 (None)
        >>  348 SEND                     3 (to 356)
            350 YIELD_VALUE
            352 RESUME                   3
            354 JUMP_BACKWARD_NO_INTERRUPT     4 (to 348)
        >>  356 POP_TOP

 81         358 LOAD_FAST                3 (codeRole)
            360 LOAD_FAST                2 (user)
            362 LOAD_ATTR                5 (roles)
            372 CONTAINS_OP              1
            374 POP_JUMP_FORWARD_IF_FALSE    28 (to 432)

 82         376 LOAD_FAST                2 (user)
            378 LOAD_METHOD             10 (add_roles)
            400 LOAD_FAST                3 (codeRole)
            402 PRECALL                  1
            406 CALL                     1
            416 GET_AWAITABLE            0
            418 LOAD_CONST               0 (None)
        >>  420 SEND                     3 (to 428)
            422 YIELD_VALUE
            424 RESUME                   3
            426 JUMP_BACKWARD_NO_INTERRUPT     4 (to 420)
        >>  428 POP_TOP
            430 JUMP_FORWARD             1 (to 434)

 84     >>  432 NOP

 87     >>  434 LOAD_FAST                1 (reaction)
            436 LOAD_ATTR               11 (message)
            446 LOAD_METHOD             12 (clear_reaction)
            468 LOAD_FAST                1 (reaction)
            470 LOAD_ATTR                7 (emoji)
            480 PRECALL                  1
            484 CALL                     1
            494 GET_AWAITABLE            0
            496 LOAD_CONST               0 (None)
        >>  498 SEND                     3 (to 506)
            500 YIELD_VALUE
            502 RESUME                   3
            504 JUMP_BACKWARD_NO_INTERRUPT     4 (to 498)
        >>  506 POP_TOP
            508 LOAD_CONST               0 (None)
            510 RETURN_VALUE
        >>  512 PUSH_EXC_INFO

 89         514 LOAD_GLOBAL              2 (discord)
            526 LOAD_ATTR               13 (HTTPException)
            536 CHECK_EXC_MATCH
            538 POP_JUMP_FORWARD_IF_FALSE    29 (to 598)
            540 STORE_FAST               5 (e)

 90         542 LOAD_GLOBAL             29 (NULL + print)
            554 LOAD_CONST               3 ('Failed to manage roles: ')
            556 LOAD_FAST                5 (e)
            558 FORMAT_VALUE             0
            560 BUILD_STRING             2
            562 PRECALL                  1
            566 CALL                     1
            576 POP_TOP
            578 POP_EXCEPT
            580 LOAD_CONST               0 (None)
            582 STORE_FAST               5 (e)
            584 DELETE_FAST              5 (e)
            586 LOAD_CONST               0 (None)
            588 RETURN_VALUE
        >>  590 LOAD_CONST               0 (None)
            592 STORE_FAST               5 (e)
            594 DELETE_FAST              5 (e)
            596 RERAISE                  1

 89     >>  598 RERAISE                  0
        >>  600 COPY                     3
            602 POP_EXCEPT
            604 RERAISE                  1

 73     >>  606 LOAD_CONST               0 (None)
            608 RETURN_VALUE
ExceptionTable:
  228 to 298 -> 512 [0]
  304 to 506 -> 512 [0]
  512 to 540 -> 600 [1] lasti
  542 to 576 -> 590 [1] lasti
  590 to 598 -> 600 [1] lasti

Disassembly of <code object on_reaction_remove at 0x564d3418c370, file "example.py", line 92>:
 92           0 RETURN_GENERATOR
              2 POP_TOP
              4 RESUME                   0

 94           6 LOAD_FAST                2 (user)
              8 LOAD_ATTR                0 (bot)
             18 POP_JUMP_FORWARD_IF_FALSE     2 (to 24)

 95          20 LOAD_CONST               0 (None)
             22 RETURN_VALUE

 97     >>   24 LOAD_GLOBAL              3 (NULL + str)
             36 LOAD_FAST                1 (reaction)
             38 LOAD_ATTR                2 (emoji)
             48 PRECALL                  1
             52 CALL                     1
             62 LOAD_FAST                0 (self)
             64 LOAD_ATTR                3 (reactions)
             74 CONTAINS_OP              0
             76 POP_JUMP_FORWARD_IF_FALSE   156 (to 390)

 98          78 LOAD_FAST                0 (self)
             80 LOAD_ATTR                3 (reactions)
             90 LOAD_GLOBAL              3 (NULL + str)
            102 LOAD_FAST                1 (reaction)
            104 LOAD_ATTR                2 (emoji)
            114 PRECALL                  1
            118 CALL                     1
            128 BINARY_SUBSCR
            138 STORE_FAST               3 (role)

100         140 NOP

101         142 LOAD_FAST                3 (role)
            144 LOAD_FAST                2 (user)
            146 LOAD_ATTR                4 (roles)
            156 CONTAINS_OP              0
            158 POP_JUMP_FORWARD_IF_FALSE    66 (to 292)

102         160 LOAD_FAST                2 (user)
            162 LOAD_METHOD              5 (remove_roles)
            184 LOAD_FAST                3 (role)
            186 PRECALL                  1
            190 CALL                     1
            200 GET_AWAITABLE            0
            202 LOAD_CONST               0 (None)
        >>  204 SEND                     3 (to 212)
            206 YIELD_VALUE
            208 RESUME                   3
            210 JUMP_BACKWARD_NO_INTERRUPT     4 (to 204)
        >>  212 POP_TOP

105         214 LOAD_FAST                1 (reaction)
            216 LOAD_ATTR                6 (message)
            226 LOAD_METHOD              7 (clear_reaction)
            248 LOAD_FAST                1 (reaction)
            250 LOAD_ATTR                2 (emoji)
            260 PRECALL                  1
            264 CALL                     1
            274 GET_AWAITABLE            0
            276 LOAD_CONST               0 (None)
        >>  278 SEND                     3 (to 286)
            280 YIELD_VALUE
            282 RESUME                   3
            284 JUMP_BACKWARD_NO_INTERRUPT     4 (to 278)
        >>  286 POP_TOP
            288 LOAD_CONST               0 (None)
            290 RETURN_VALUE

101     >>  292 LOAD_CONST               0 (None)
            294 RETURN_VALUE
        >>  296 PUSH_EXC_INFO

107         298 LOAD_GLOBAL             16 (discord)
            310 LOAD_ATTR                9 (HTTPException)
            320 CHECK_EXC_MATCH
            322 POP_JUMP_FORWARD_IF_FALSE    29 (to 382)
            324 STORE_FAST               4 (e)

108         326 LOAD_GLOBAL             21 (NULL + print)
            338 LOAD_CONST               1 ('Failed to manage roles: ')
            340 LOAD_FAST                4 (e)
            342 FORMAT_VALUE             0
            344 BUILD_STRING             2
            346 PRECALL                  1
            350 CALL                     1
            360 POP_TOP
            362 POP_EXCEPT
            364 LOAD_CONST               0 (None)
            366 STORE_FAST               4 (e)
            368 DELETE_FAST              4 (e)
            370 LOAD_CONST               0 (None)
            372 RETURN_VALUE
        >>  374 LOAD_CONST               0 (None)
            376 STORE_FAST               4 (e)
            378 DELETE_FAST              4 (e)
            380 RERAISE                  1

107     >>  382 RERAISE                  0
        >>  384 COPY                     3
            386 POP_EXCEPT
            388 RERAISE                  1

 97     >>  390 LOAD_CONST               0 (None)
            392 RETURN_VALUE
ExceptionTable:
  142 to 286 -> 296 [0]
  296 to 324 -> 384 [1] lasti
  326 to 360 -> 374 [1] lasti
  374 to 382 -> 384 [1] lasti