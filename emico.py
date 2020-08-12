import os

def write_cmake_file(src_paths: list):
	cmake = open('CMakeLists.txt', 'w+')
	cmake.write('cmake_minimum_required(VERSION 3.16)\n')
	cmake.write('project(emico)\n')
	cmake.write('include_directories(include)\n')
	cmake.write('add_library(\n')
	cmake.write('\temico\n')
	cmake.write('\tSTATIC\n')
	cmake.write('\tsrc/emico.cpp\n')
	print(len(src_paths), 'sources to list.')
	for path in src_paths:
		cmake.write('\t' + path + '\n')
	cmake.write(')\n')

def write_primary_source_file(symbols: list):
	psrc = open('src/emico.cpp', 'w+')
	psrc.write('#include <emico.h>\n')
	for buncha in symbols:
		psrc.write(buncha[1] + ';\n')
		psrc.write(buncha[2] + ';\n')
	psrc.write('const std::map<std::string, std::pair<const void *, unsigned int>> emico::assets {\n')
	psrc.write(',\n'.join(['\t{ "%s", { %s, %s } }' % (x[0], x[1].split('extern const unsigned char *')[1], x[2].split('extern const unsigned int ')[1]) for x in symbols]))
	psrc.write('\n};\n')

def begin(path: str):
	symbols = []
	src_paths = []
	for category in os.listdir(path):
		if not os.path.isdir(path + '/' + category):
			continue
		for src_file in process_asset_category_root(path + '/' + category, category, symbols):
			src_paths.append(src_file)
	write_cmake_file(src_paths)
	write_primary_source_file(symbols)

def process_asset_category_root(path: str, category: str, symbols):
	src_paths = []
	print('asset category root ->', path, category)
	for entry in os.listdir(path):
		if os.path.isdir(path + '/' + entry):
			for src_file in process_asset_category_root(path + '/' + entry, category + '.' + entry, symbols):
				src_paths.append(src_file)
		elif os.path.isfile(path + '/' + entry):
			src_paths.append(transcribe_asset(path + '/' + entry, entry, category))
			p_symbol = ('%s_%s' % (category, entry)).replace('.', '_')
			begin_symbol = 'extern const unsigned char *g_emico_' + p_symbol + '_data'
			size_symbol = 'extern const unsigned int g_emico_' + p_symbol + '_size'
			symbols.append((category + '.' + entry, begin_symbol, size_symbol))
	return src_paths

def transcribe_asset(path: str, entry:str, category: str):
	print('\t transcribe -> (' + path + ')', entry, '->', category)
	os.makedirs('src/' + category.replace('.', '/'), exist_ok=True)
	src_file = 'src/' + category.replace('.', '/') + '/' + entry + '.cpp'
	src = open(src_file, 'w+')
	src.write('#define INCBIN_STYLE INCBIN_STYLE_SNAKE\n')
	src.write('#include <incbin.h>\n')
	src.write('INCBIN(_emico_%s, "../%s");\n' % ((category + '_' + entry).replace('.', '_'), path))
	return src_file

if __name__ == "__main__":
	begin('assets')