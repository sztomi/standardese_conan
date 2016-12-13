#include <standardese/parser.hpp>
#include <standardese/translation_unit.hpp>
#include <spdlog/spdlog.h>

#include <stdio.h>
#include <fstream>
#include <cstdio>

inline standardese::compile_config get_compile_config() {
  standardese::compile_config c(standardese::cpp_standard::cpp_14);
#ifdef _MSC_VER
    c.set_flag(standardese::compile_flag::ms_compatibility);
    c.set_flag(standardese::compile_flag::ms_extensions);
    c.set_msvc_compatibility_version(_MSC_VER / 100u);
#endif
    return c;
}

inline standardese::translation_unit parse(standardese::parser &p,
                                           const char *name, const char *code) {
  std::ofstream file(name);
  file << code;
  file.close();

  auto tu = p.parse(name, get_compile_config());
  std::remove(name);
  return tu;
}

int main() {
    auto logger = spdlog::stdout_logger_mt("mylogger", true);
    standardese::parser p(logger);
    auto code = R"(
            /// A function.
            void foo();
            /// A class.
            struct bar {};
    )";
    auto tu = parse(p, "output_filename", code);
    std::cout << tu.get_file().get_name().c_str() << "\n";
    return 0;
}

