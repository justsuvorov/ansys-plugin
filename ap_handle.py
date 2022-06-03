from ap_parameters import APParameters
from WBInterface import WBInterface
from Logger import Logger

"""
A class to handle WB project
iterationCount is the required number of iterations
iterationBuilder is the module for solving several problems, for example, optimization problem
"""
class APHandle:
	def __init__(self,
		fileName,
        parameters,
		wb,
		iterationCount,
		iterationBuilder = None
	):
		self._logger = Logger('log.txt')
		self._log_ = self._logger.log
		self.__fileName = fileName
		self.__wb = wb
		self.__parameters = parameters
		self.__iterationCount = iterationCount
		self.__iterationBuilder = iterationBuilder
		self._log_('[APHandle]: ' + self.__class__.__name__)

	''''''
	def run(self):
		try:
			self.__wb.open_any(archive_first=True)
			# self.__wb.find_and_import_parameters()
				#----------------------------------------------------------------
				# Parameters can be imported directly
			self._log_('[APHandle.run] __iterationCount: ' + str(self.__iterationCount))
			self._log_('[APHandle.run] __iterationBuilder: ' + str(self.__iterationBuilder))
			for index in range(self.__iterationCount):
				self._log_('[APHandle.run] iteration index: ' + str(index))
				outParamsStr = self.__solveProject(
					self.__parameters.inputP(),
					self.__parameters.outputP()
				)
				outParams = []
				for rowStr in outParamsStr:
					row = []
					for item in rowStr:
						row.append(float(item))
					outParams.append(row)
				self.__parameters = self.__iterationBuilder(
					index = index,
					outParams = outParams
				)
				self._log_('[APHandle.run] iteration ' + str(index) + ' completed')

			self._log_('[APHandle.run] all ' + str(self.__iterationCount) + ' iterations completed')
			self._log_('[APHandle.run] writing report...')
			self.__wb.export_wb_report()
			with open('file.txt', 'w') as f:
				print >> f, outParams

			#self._log_('[APHandle.run] outParams:')
			self._log_(outParams)


		except Exception as err_msg:

			self.__wb.fatal_error(err_msg)

		finally:

			#self.__wb.archive_if_complete()

			self.__wb.issue_end()


	def __solveProject(self,
	   inputP,
	   outputP
	):
		#self._log_('[APHandle.__solveProject]')
		# input_p = {
			# 'p83':[1,0.1,0.5,0.6],
			# 'p84':[1,0.1,0.5,0.6],
			# 'p85':[1,0.1,0.5,0.6],
		# }
		self.__wb.input_by_name(
			inputP
			# input_p
		)

		self.__wb.import_parameters()

		# output_p = ['p36']
		self.__wb.set_output(
			outputP
			# output_p
		)
			#==============================================================================
			# Sets maximum number of cores
			# self.__wb.set_cores_number('SYS')

			# Activate distrubuted solver
			# self.__wb.set_distributed('SYS', True)

			# Sets unit system
			# self.__wb.set_unit_system('SYS', unit_sys='NMM')
			#==============================================================================

		self.__wb.update_project()

			#==============================================================================
			# Set figure scale
			# self.__wb.set_figures_scale('SYS', scale='auto')
			# self.__wb.show_all_bodies('SYS')

			# Picture parameters
			# overview_args = dict(width=1920, height=1080, zoom_to_fit=True, view='iso')
			# mesh_args = dict(width=1920*2, height=1080*2, zoom_to_fit=True, view='iso')
			# env_args = dict(width=1920, height=1080, zoom_to_fit=True, fontfact=1.5, view='iso')
			# fig_args = dict(width=1920, height=1080, zoom_to_fit=True, fontfact=1.35, view='iso', shade_mode='ShowWireframe')
			# ani_args = dict(width=1920/2, height=1080/2, zoom_to_fit=True, scale='auto', frames=20, view='iso', shade_mode='ShowWireframe')


			# Save pictures parameters
			# self.__wb.save_overview('SYS', cwdp('pictures'), 'model_overview.jpg', **overview_args)
			# self.__wb.save_mesh_view('SYS', cwdp('pictures'), 'mesh.png', **mesh_args)
			# self.__wb.save_setups_view('SYS', cwdp('pictures'), **env_args)
			# self.__wb.save_figures('SYS', cwdp('pictures'), **fig_args)
			# self.__wb.save_animations('SYS', cwdp('animations'), **ani_args)

			#----------------------------------------------------------------
			# Can also save for each Design Point
			# for i, dp in enumerate(self.__wb.DPs):
				# self.__wb.set_active_DP(dp)

				# mesh_file = 'mesh_DP{}.png'.format(i)
				# mesh_args = dict(width=1920*2, height=1080*2, zoom_to_fit=True)
				# self.__wb.save_mesh_view('SYS', cwdp('pictures'), mesh_file, **mesh_args)

				# fig_pref = 'Result_DP{}'.format(i)
				# fig_args = dict(fpref=fig_pref, width=1920*2, height=1080*2, zoom_to_fit=True, fontfact=1.35)
				# self.__wb.save_figures('SYS', cwdp('pictures'), **fig_args)

				# env_pref = 'Setup_DP{}'.format(i)
				# env_args = dict(fpref=env_pref, width=1920, height=1080, zoom_to_fit=True, fontfact=1.5)
				# self.__wb.save_setups_view('SYS', cwdp('pictures'), **env_args)
			#==============================================================================
		self._log_('[APHandle.__solveProject] completed')
		return self.__wb.output_parameters()