# emico

For when you have many many many large or small files that you'd rather neatly tuck away inside the binary.

#### Sample
``` c++
#include <emico.h>
#include <iostream>

using std::cout;
using std::endl;

int main() {

	cout << "There are " << emico::assets.size() << " embedded assets." << endl;

	for (auto &asset : emico::assets) {
		
		cout << "\t" << asset.first << // Unique ID based on the original file path.
			" : " << asset.second.first << // The memory address of the file contents.
			" (" << asset.second.second << " bytes)" << endl; // Length in bytes of the content.
	}
}
```
#### Output
```
There are 2 embedded assets.
	metadata.things.txt : 0x74616420656d6f53 (39 bytes)
	textures.hye2o8un1rq11.png : 0xa1a0a0d474e5089 (5846127 bytes)
```

### Procedure
Run ```python3 emico.py```. The script will use the masterfully crafted [**incbin**](https://github.com/graphitemaster/incbin) to embed the file contents into individual ```.cpp``` source files. It will also generate an appopriate ```CMakeLists.txt``` for you.

Here's what the assets directory looked like in the above sample output:

<pre><font color="#3465A4"><b>.</b></font>
├── <font color="#3465A4"><b>metadata</b></font>
│   └── things.txt
└── <font color="#3465A4"><b>textures</b></font>
    └── <font color="#75507B">hye2o8un1rq11.png</font></pre>

The root level must be always a folder but you can have as many files and folders underneath as your heart desires.

#### Check if an item exists

Since the ```map``` is constant, use ```.find()``` to get a specific item:

``` c++
if (auto data = emico::assets.find("shaders.cartoon.glsl"); data != emico::assets.end()) {
	data -> ...
}
```

### Specifics

Here's an example of what the generate **```emico.cpp```** will look like:

``` c++
#include <emico.h>
extern const unsigned char *g_emico_metadata_things_txt_data;
extern const unsigned int g_emico_metadata_things_txt_size;
extern const unsigned char *g_emico_textures_hye2o8un1rq11_png_data;
extern const unsigned int g_emico_textures_hye2o8un1rq11_png_size;
const std::map<std::string, std::pair<const void *, unsigned int>> emico::assets {
	{ "metadata.things.txt", { g_emico_metadata_things_txt_data, g_emico_metadata_things_txt_size } },
	{ "textures.hye2o8un1rq11.png", { g_emico_textures_hye2o8un1rq11_png_data, g_emico_textures_hye2o8un1rq11_png_size } }
};
```

Those extern's are defined in the many many other source files that are generated to represent each file. Here's **```src/hye2o8un1rq11.png.cpp```**:

``` c++
#define INCBIN_STYLE INCBIN_STYLE_SNAKE
#include <incbin.h>
INCBIN(_emico_textures_hye2o8un1rq11_png, "../assets/textures/hye2o8un1rq11.png");
```

Super simple and saves loads of time.
