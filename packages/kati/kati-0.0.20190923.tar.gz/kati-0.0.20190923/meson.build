project(
  'kati',
  'cpp',
  default_options: ['cpp_std=c++17'],
  version: '0.0.20190923',
)

add_project_arguments('-DNOLOG', '-U_GLIBCXX_ASSERTIONS', language: 'cpp')

cc = meson.get_compiler('cpp')

executable(
  'ckati',
  [
    'src/affinity.cc',
    'src/command.cc',
    'src/dep.cc',
    'src/eval.cc',
    'src/exec.cc',
    'src/expr.cc',
    'src/file.cc',
    'src/file_cache.cc',
    'src/fileutil.cc',
    'src/find.cc',
    'src/flags.cc',
    'src/func.cc',
    'src/io.cc',
    'src/log.cc',
    'src/main.cc',
    'src/ninja.cc',
    'src/parser.cc',
    'src/regen.cc',
    'src/regen_dump.cc',
    'src/rule.cc',
    'src/stats.cc',
    'src/stmt.cc',
    'src/stringprintf.cc',
    'src/strutil.cc',
    'src/symtab.cc',
    'src/timeutil.cc',
    'src/var.cc',
    'src/version_unknown.cc',
  ],
  dependencies: [
    cc.find_library('pthread', required: false),
    cc.find_library('rt', required: false),
  ],
  install: true,
)
