$(TOP)/mk/gen/phony-list.mk: $(patsubst ./%,$(TOP)/%,$(filter-out %.d,  mk/main.mk mk/check-env.mk mk/gen/allowed-variables.mk mk/configure.mk config.mk mk/defaults.mk mk/lib.mk mk/paths.mk mk/support/build.mk mk/install.mk drivers/build.mk drivers/javascript/build.mk drivers/python/build.mk drivers/ruby/build.mk drivers/java/build.mk admin/build.mk src/build.mk mk/packaging.mk mk/tools.mk test/build.mk))
PHONY_LIST += default-goal all FORCE sense love fetch support fetch-node build-node clean-node shrinkwrap-node support-node support-node_0.12.2 clean-node_0.12.2 fetch-coffee-script build-coffee-script clean-coffee-script shrinkwrap-coffee-script support-coffee-script support-coffee-script_1.10.0 clean-coffee-script_1.10.0 fetch-browserify build-browserify clean-browserify shrinkwrap-browserify support-browserify support-browserify_12.0.1 clean-browserify_12.0.1 fetch-bluebird build-bluebird clean-bluebird shrinkwrap-bluebird support-bluebird support-bluebird_2.9.32 clean-bluebird_2.9.32 fetch-admin-deps build-admin-deps clean-admin-deps shrinkwrap-admin-deps support-admin-deps support-admin-deps_2.0.3 clean-admin-deps_2.0.3 fetch-gtest build-gtest clean-gtest shrinkwrap-gtest support-gtest support-gtest_1.7.0 clean-gtest_1.7.0 fetch-v8 build-v8 clean-v8 shrinkwrap-v8 support-v8 support-v8_3.30.33.16 clean-v8_3.30.33.16 fetch-re2 build-re2 clean-re2 shrinkwrap-re2 support-re2 support-re2_20140111 clean-re2_20140111 fetch-openssl build-openssl clean-openssl shrinkwrap-openssl support-openssl support-openssl_1.0.1t clean-openssl_1.0.1t fetch-jemalloc build-jemalloc clean-jemalloc shrinkwrap-jemalloc support-jemalloc support-jemalloc_4.1.0 clean-jemalloc_4.1.0 support-include-v8 support-include-v8_3.30.33.16 support-include-gtest support-include-gtest_1.7.0 support-include-openssl support-include-openssl_1.0.1t support-include-openssl support-include-openssl_1.0.1t support-include-re2 support-include-re2_20140111 support-include-openssl support-include-openssl_1.0.1t support-include-jemalloc support-include-jemalloc_4.1.0 install-binaries install-manpages install-init install-config install-data install-docs install js-dist js-publish js-clean js-install js-dependencies js-driver py-driver py-clean py-sdist py-bdist py-publish py-install rb-driver rb-sdist rb-publish rb-clean java-driver java-clean clean-autogenerated java-convert-tests java-test update-driver drivers drivers/all web-assets-watch web-assets src/all unit rethinkdb deps build-clean check-syntax prepare_deb_package_dirs build-deb-src deb-src-dir build-deb install-osx build-osx clean-dist-dir reset-dist-dir dist-dir dist tags etags cscope test-deps test full-test clean))
