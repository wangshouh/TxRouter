import re

input_calldata = """
[5]:  000000000000000000000000d483bad325523e7af9004c74d9a330fd9cb54b2b
[6]:  000000000000000000000000000000000000000000000006c6b935b8bbd40000
[7]:  0000000000000000000000006760d6160e7160d4b00e53345ec10ff148e07d86
[8]:  000000000000000000000000000000000000000000000006c6b935b8bbd40000
[9]:  000000000000000000000000e3d7a60b3c3739cf4350b57fc60b968699639d89
[10]: 000000000000000000000000000000000000000000000006c6b935b8bbd40000
[11]: 000000000000000000000000095540db438aff31dbcf5ae0c72e72a4f3c733aa
[12]: 0000000000000000000000000000000000000000000000052663ccab1e1c0000
[13]: 000000000000000000000000257abf62ab81944fffbffd20be3b2a0d9c10403c
[14]: 000000000000000000000000000000000000000000000004be4e7267b6ae0000
[15]: 000000000000000000000000398e1ff63d2c1c009c4871c1175e443236e19e60
[16]: 0000000000000000000000000000000000000000000000046791fc84e07d0000
[17]: 0000000000000000000000009118ca7cc8fdc1f4c18e4ba9bbde6c69de0ea29d
[18]: 0000000000000000000000000000000000000000000000046791fc84e07d0000
[19]: 0000000000000000000000001d800a021f1434baffe3d51afe5200b353b7a677
[20]: 000000000000000000000000000000000000000000000003860e639d80640000
[21]: 000000000000000000000000c7752dd1df8f2e85fd9cb8884916647e104fb99b
[22]: 000000000000000000000000000000000000000000000003635c9adc5dea0000
[23]: 000000000000000000000000f03342e0c5983d124b7652ab13b09524df2e3685
[24]: 0000000000000000000000000000000000000000000000030ca024f987b90000
[25]: 0000000000000000000000000b8d39753a2500fefb4183e5031579238becb9c2
[26]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[27]: 000000000000000000000000b66c313a4945456cb9828b363c89262df6ef8734
[28]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[29]: 000000000000000000000000d5361f04b90d56cc48fb5ba9da7acf5f25f2f363
[30]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[31]: 00000000000000000000000001a2b6c749b778053bc81551e23675f0aee641dc
[32]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[33]: 000000000000000000000000739e576b1ffe804cef026bc914f5f2edce414dfb
[34]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[35]: 0000000000000000000000005e331d09974b95b3b1c6d31c49b21bfe5082fd11
[36]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[37]: 000000000000000000000000c45e9d4c43c622bf215c9270172174fd63921ab7
[38]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[39]: 0000000000000000000000004062cfa41b1be30db8820f87eec2102bbd64abd7
[40]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[41]: 000000000000000000000000c0f8ab7741786537845716cdf9c42507f2e53da4
[42]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[43]: 000000000000000000000000c4acff2d5967eb56acff7f2bf3975f13e465cf71
[44]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[45]: 00000000000000000000000025bddc414deb77bf8ad9611456ac28f76a1c2134
[46]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[47]: 000000000000000000000000d43b78dd7b411615954bdcbe882a3d31eac4bc9d
[48]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[49]: 0000000000000000000000001a59fb41677e7cb442812f1b990249cede01507c
[50]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[51]: 0000000000000000000000005ab655f7026cef1722f57dffeb231a34b3e69e78
[52]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[53]: 000000000000000000000000515bb2c65f70c7a647a802b439e2a0e128ac67df
[54]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[55]: 0000000000000000000000003f1f7ee171f838c203aed2e2aca010fc0cfcb24c
[56]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[57]: 000000000000000000000000d46ccc0abab29e49e514fc741d35aa632bf57915
[58]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[59]: 00000000000000000000000053d9b98b1a69a89f52c1e8fee760bb3cc6b34264
[60]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[61]: 0000000000000000000000009eb30511458ab8b26695a8404e439444836bc07d
[62]: 000000000000000000000000000000000000000000000002b5e3af16b1880000
[63]: 000000000000000000000000b54c0a734536cc97c3b192709062ef7a5d238059
[64]: 000000000000000000000000000000000000000000000001e5b8fa8fe2ac0000
[65]: 000000000000000000000000f49d401d7a66677150df28e9f6fa2d0e3f28a22d
[66]: 000000000000000000000000000000000000000000000001b1ae4d6e2ef50000
[67]: 000000000000000000000000c34e0727428303010eef33dfe026e0d175f430a3
[68]: 000000000000000000000000000000000000000000000001b1ae4d6e2ef50000
[69]: 000000000000000000000000f1ea6ad49aabb2e2c462e64338483da663c60027
[70]: 000000000000000000000000000000000000000000000001b1ae4d6e2ef50000
[71]: 0000000000000000000000003e9b28e46af3ca5cd64bafcec1c088937423721a
[72]: 000000000000000000000000000000000000000000000001b1ae4d6e2ef50000
[73]: 00000000000000000000000003b0fdf66d3d3a9f02d4e27742318c13de27bece
[74]: 000000000000000000000000000000000000000000000001a055690d9db80000
[75]: 00000000000000000000000039752b695e4a6b2074772ebe9a6806e11742e99c
[76]: 000000000000000000000000000000000000000000000001a055690d9db80000
[77]: 000000000000000000000000c7cd47182acfac57a33c61e8388a1fe4a6d4583e
[78]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[79]: 000000000000000000000000831726cb1f52951a729c68e322748df7e4896311
[80]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[81]: 000000000000000000000000e6414df6a6ff4470c4593ba043296a8482141c7d
[82]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[83]: 000000000000000000000000b243a4024086f41b6a50b71cfa09a8fe6154fc5d
[84]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[85]: 000000000000000000000000d2be9a87625cbc584e52508d1f3eea9c174a13ae
[86]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[87]: 0000000000000000000000008606a682d2c5a6427d1879c1a960dd3ccd127d35
[88]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[89]: 0000000000000000000000007f921eeef2eb748f114f1829bd2189ff705c06d5
[90]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[91]: 0000000000000000000000003131d9e8d4d1c56eb3fcd68c84b11aa6a627725f
[92]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[93]: 000000000000000000000000cc43c0cef2afd62a0d89850215ee72656ec7c261
[94]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[95]: 000000000000000000000000cc4f1c14bb56cde9326260986817db031b33afd1
[96]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[97]: 0000000000000000000000001d6f461224226f2bb70b7f1d004afa8ca23ac73f
[98]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[99]: 00000000000000000000000029cae646b6eb3377db9829cb05997975d4e5e8f9
[100]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[101]: 0000000000000000000000003ba451151e5040b52d3e27919d3f93f335122323
[102]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[103]: 000000000000000000000000cb3b71a733759c56378c23bbab43e8fb85ccbdf2
[104]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[105]: 00000000000000000000000034f593a8fb2fcc8f8c88bd77524ccbaa44570dc2
[106]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[107]: 000000000000000000000000cdd94ad6802de4c27fbf57469206af6921e70175
[108]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[109]: 000000000000000000000000766fc0dd3efc2dc1058763209cae3776cedff047
[110]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[111]: 0000000000000000000000006ecdbfa544fb064550d9929fc7539f61dfb4c55d
[112]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[113]: 000000000000000000000000d0837af82052e02a5d72730b33c26c893ffa2b93
[114]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[115]: 0000000000000000000000009a2b46bcd1c0015caa9b0ea9ccc6a01bcb4e8e22
[116]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[117]: 000000000000000000000000097e361a32e037f35d154d19221ecba443cebdbb
[118]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[119]: 00000000000000000000000091abb587fb0ce16381992c6ae2d7af4da59a050d
[120]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[121]: 0000000000000000000000009e600844f5722f09b2f1f4aa458482595924d726
[122]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[123]: 00000000000000000000000076532473ba126ac1cc621aee62651d57e500a0f4
[124]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[125]: 0000000000000000000000003fa6b47e844495d9949bf7fe7ae0ab7b2a742896
[126]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[127]: 000000000000000000000000d6f6a387019961592c97670fc4c243f5fc6d2153
[128]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[129]: 0000000000000000000000007034d42b51ce7ad2a0277451e296b650b932d982
[130]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[131]: 000000000000000000000000e06f67ea03723c695b6274f8a52f0e32a1c1e3bb
[132]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[133]: 0000000000000000000000009dd79861746ca05923e0daf029b7ecf328739fcc
[134]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[135]: 00000000000000000000000014657b1aa49c653e547a26cfe0deb3d7386c37c1
[136]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[137]: 000000000000000000000000fc944a99a2e0e8c9e69440ed1fc1b348df5807f7
[138]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[139]: 000000000000000000000000aef3b28e938166ce4740d9d32e63b7f36dc52ca2
[140]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[141]: 000000000000000000000000f26bbdc8c4a433fc488f2a297934397348f3b33b
[142]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[143]: 000000000000000000000000eaa8839cf576297d580eba026347a7d7f128163a
[144]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
[145]: 0000000000000000000000009c449094c105cdd5c1dc064c546d983894af8bac
[146]: 0000000000000000000000000000000000000000000000008ac7230489e80000
[147]: 000000000000000000000000ac448c77ba5709888b5cfcf1d5b022903343e022
[148]: 0000000000000000000000000000000000000000000000015af1d78b58c40000
"""

clean_calldata = []

for input_str in input_calldata.split("\n"):
	if input_str == "":
		continue
	else:
		output_str = re.sub(r"\[[^\]]*\]:\s*", "", input_str)

		clean_calldata.append(output_str)

output_list = []

for i in range(0, len(clean_calldata), 2):
    output_list.append(clean_calldata[i][24:] + clean_calldata[i+1][40:])

output_string = ','.join(output_list)

print(output_string)