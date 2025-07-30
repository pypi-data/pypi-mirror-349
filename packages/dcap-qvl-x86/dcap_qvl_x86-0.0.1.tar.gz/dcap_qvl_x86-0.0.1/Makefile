WASM_PACK = wasm-pack
INSTALL_TOOL = curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
BUILD_WEB = $(WASM_PACK) build --release --target web --out-dir pkg/web --out-name dcap-qvl-web -- --features=js
BUILD_NODE = $(WASM_PACK) build --release --target nodejs --out-dir pkg/node --out-name dcap-qvl-node -- --features=js
BUILD_PYTHON = maturin build --release --features=python

all: install_wasm_tool build_web_pkg build_node_pkg build_python_pkg

install_wasm_tool:
	@echo "Installing wasm-pack if not already installed..."
	@if ! command -v $(WASM_PACK) &> /dev/null; then \
		echo "wasm-pack not found, installing..."; \
		$(INSTALL_TOOL); \
	else \
		echo "wasm-pack is already installed."; \
	fi

build_web_pkg: install_wasm_tool
	@echo "Building for web browsers..."
	$(BUILD_WEB)

build_node_pkg: install_wasm_tool
	@echo "Building for Node.js..."
	$(BUILD_NODE)

build_python_pkg: install_wasm_tool
	@echo "Building Python package..."
	$(BUILD_PYTHON)

clean:
	@echo "Cleaning up..."
	rm -rf pkg target

.PHONY: all install_wasm_tool build_web_pkg build_node_pkg build_python_pkg clean
