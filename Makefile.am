
include $(top_srcdir)/Common.am

ACLOCAL_MFLAGS = -I m4

SUBDIRS = lib src plugins commands tests

EXTRA_DIST = install_libs.py install_modules.py nova-agent.py \
			run_tests.py patch_binary.py scripts/agent-smith \
			scripts/generic/nova-agent scripts/gentoo/nova-agent \
			scripts/freebsd/nova-agent

data_DATA = nova-agent.py

nodist_noinst_DATA = agentlib.so \
			scripts/installer.sh \
			scripts/generic/nova-agent \
			scripts/gentoo/nova-agent \
			scripts/freebsd/nova-agent

noinst_DATA = scripts/generic/nova-agent.in \
		scripts/gentoo/nova-agent.in \
		scripts/freebsd/nova-agent.in

agentlib.so:
	    ln -s lib/.libs/agentlib.so agentlib.so

BINTARDIR = @PACKAGE@-`uname -s`-`uname -m`-@PACKAGE_VERSION@
BINTARNAME = ${BINTARDIR}.tar.gz
FULLBINTARDIR = $(top_srcdir)/${BINTARDIR}

check-local:
	@${PYTHON_VER} run_tests.py

install-exec-local: install-modules install-libs patch-binary
	rm -f ${DESTDIR}${datadir}/../nova-agent.py
	ln -s ${datadir}/nova-agent.py ${DESTDIR}${datadir}/../nova-agent.py
#	@$(PYTHON_VER) $(top_srcdir)/patch_libs.py ${DESTDIR}${datadir} $(libdir)

install-modules:
	@$(PYTHON_VER) $(top_srcdir)/install_modules.py ${DESTDIR}$(modulesdir)

install-libs:
	@$(PYTHON_VER) $(top_srcdir)/install_libs.py ${DESTDIR}$(sbindir)/nova-agent $(DESTDIR)${datadir} ${DESTDIR}/$(libdir)

patch-binary:
	@$(PYTHON_VER) $(top_srcdir)/patch_binary.py ${DESTDIR}${sbindir}/nova-agent ${DESTDIR} $(libdir)

distclean-local:
	rm -f $(top_srcdir)/{configure,configure.in}
	rm -f $(top_srcdir)/{aclocal.m4,compile,config.guess,config.sub}
	rm -f $(top_srcdir)/{depcomp,install-sh,ltmain.sh,missing}
	find $(top_srcdir) -name Makefile.in -exec rm -f {} \;
	find $(top_srcdir) -name configure.in -exec rm -f {} \;
	rm -rf $(top_srcdir)/m4
	rm -rf $(top_srcdir)/autom4te.cache

clean-local::
	rm -f agentlib.so
	find . -name '*.gcov' -delete -o -name '*.gcda' -delete -o -name '*.gcno' -delete
	find . -name '*.pyc' -exec rm -f {} \;
	rm -rf $(top_srcdir)/${BINTARDIR}

coverage:: check
	for d in $(SUBDIRS) ; do cd $$d ; for f in *.c ; do gcov $$f; done ; cd ..; done

bintar: all
	@rm -rf ${FULLBINTARDIR}
	@mkdir -m 0755 ${FULLBINTARDIR} ${FULLBINTARDIR}/${prefix}
	@mkdir -m 0755 ${FULLBINTARDIR}/${prefix}/{share,sbin}
	@$(MAKE) install DESTDIR=$(CURDIR)/${BINTARDIR}
	@chmod -R go-rwx ${FULLBINTARDIR}/${datadir}
	@cp $(top_srcdir)/scripts/agent-smith ${FULLBINTARDIR}/${prefix}/sbin/.
	@chmod 700 ${FULLBINTARDIR}/${prefix}/sbin/agent-smith
	@cp $(top_srcdir)/scripts/installer.sh ${FULLBINTARDIR}/.
	@chmod 700 ${FULLBINTARDIR}/installer.sh
	@mkdir -m 0700 ${FULLBINTARDIR}/${etcdir}
	@mkdir -m 0700 ${FULLBINTARDIR}/${etcdir}/generic
	@mkdir -m 0700 ${FULLBINTARDIR}/${etcdir}/gentoo
	@mkdir -m 0700 ${FULLBINTARDIR}/${etcdir}/freebsd
	@install -m 700 $(top_srcdir)/scripts/generic/nova-agent ${FULLBINTARDIR}/${etcdir}/generic/nova-agent
	@install -m 700 $(top_srcdir)/scripts/gentoo/nova-agent ${FULLBINTARDIR}/${etcdir}/gentoo/nova-agent
	@install -m 700 $(top_srcdir)/scripts/freebsd/nova-agent ${FULLBINTARDIR}/${etcdir}/freebsd/nova-agent
	@chown -R 0:0 ${FULLBINTARDIR}
# agent-smith requires that we don't have a subdir in the tar
# once agent-smith is dead, we can use this
#	@tar -czf $(top_srcdir)/${BINTARNAME} -C $(CURDIR) ${BINTARDIR}
	@tar -czf $(top_srcdir)/${BINTARNAME} -C $(CURDIR)/${BINTARDIR} .
	@rm -rf ${FULLBINTARDIR}
	@echo ""
	@echo "Created $(BINTARNAME)"
	@echo ""
