#!/usr/bin/env python 
#-*- coding: UTF-8 -*- 
#=================================================================================================================
import tensorflow as tf
import common
from utils import varDef
from mainArgs import *
tf_float_ = tf.float32

#=================================================================================================================

## MHC onehot matrice 进行编码
def encode_onehot_mhc_by_cnn(onehot_mhc, filters, regularizer):
	"""cnn编码mhc的01矩阵
	args:
		onehot_mhc: shape = [BATCH_SIZE, 5*mhc_length]
		filters: shape = [MHC_KERNEL_HEIGHT_LIST, MHC_FILTER_DEPTH, MHC_FILTER_WIDTH]
	return:
		代表MHC特征的一个结构固定的矩阵，shape = [MHC_HEIGHT, MHC_WIDTH]
	"""
	pass
	return

def encode_onehot_mhc_by_rnn(onehot_mhc, hidden_size, regularizer):
	"""rnn编码mhc的01矩阵
	args:
		onehot_mhc: shape = [BATCH_SIZE, 5*mhc_length]
		hidden_size: shape = [MHC_HIDDEN_SIZE]
	return:
		MHC的特征矩阵：shape = [BATCH_SIZE, MHC_HEIGHT*MHC_WIDTH]
	"""
	pass
	return
	
#=================================================================================================================
## 实现肽段特征矩阵到突变表征矩阵的映射
def run_convRNN(mhc, peps, regularizer):
	"""
	args:
		mhc: shape = [BATCH_SIZE, 特征矩阵长x宽]
		peps: shape = [BATCH_SIZE, NUM_PEPGROUP, 特征矩阵长x宽]
	return:
		NUM_PEPGROUP个R矩阵，shape = [BATCH_SIZE, NUM_PEPGROUP, MUTMAT_HEIGHT*MUTMAT_WIDTH]
	"""
	pass
	return

#=================================================================================================================
## 由突变表征矩阵生成新的肽段特征矩阵
def run_multiRNN(mhc, normal_peps, regularizer):
	"""
	args:
		mhc: shape = [BATCH_SIZE, 特征矩阵长x宽] 初始化
		normal_peps: shape = [BATCH_SIZE, NUM_PEPGROUP, MUTMAT_HEIGHT*MUTMAT_WIDTH] R矩阵
	return:
		new_peps: shape = [BATCH_SIZE, ]
	"""
	pass
	return
	
#=================================================================================================================
## 混合高斯采样
def mixed_guassian_sampling(gmm_args):
	"""
	args:
		gmm_args: 分布参数
	return:
		一系列分布矩阵
	"""
	pass
	return
	
#=================================================================================================================
## 计算分布损失
def calc_loss_of_distribution(mutmats, gmm_args):
	"""
	args:
		mutmats: 突变表征矩阵,shape = [BATCH_SIZE, MUTMAT_HEIGHT*MUTMAT_WIDTH]
		gmm_args: 混合高斯分布的参数list
	return:
		distribution_loss: 隐藏分布和真实分布间距离造成的损失
	"""
	gmm_samples = mixed_guassian_sampling(gmm_args)
	pass
	return

#=================================================================================================================
## 计算ic50
def calc_ic(mhc, new_peps, regularizer):
	"""
	args:
		new_peps: shape = [BATCH_SIZE, NUM_PEPGROUP, PEP_HEIGHT*PEP_WIDTH]
		mhc: shape = [BATCH_SIZE, MHC_HEIGHT*MHC_WIDTH]
	return:
		ic_values: shape = [BATCH_SIZE, NUM_PEPGROUP]
	"""
	pass
	return
	
#=================================================================================================================
## 计算生成peps损失
def calc_loss_of_peps(real_peps, gene_ics):
	"""
	args:
		real_peps:	shape = [BATCH_SIZE, NUM_PEPGROUP, PEP_HEIGHT*PEP_WIDTH]
		gene_peps:	shape = [BATCH_SIZE, NUM_PEPGROUP, PEP_HEIGHT*PEP_WIDTH]		
	return：
		losses
	"""
	pass
	return
	
#=================================================================================================================
## 计算生成ics损失
def calc_loss_of_ics(real_ics, gene_ics):
	"""
	args:
		real_ics: 	shape = [BATCH_SIZE, NUM_PEPGROUP]
		gene_ics:	shape = [BATCH_SIZE, NUM_PEPGROUP]
	return：
		losses
	"""
	pass
	return

#=================================================================================================================
## Forward propagation	
def inference(onehot_mhc, fixed_mats, regularizer):
	"""Forward propagation.
	Training or utilizing depends on whether 'regularizer' is None, and None means utilizing.
	args:
		onehot_mhc: shape = [BATCH_SIZE, 5*mhc_length] or other
		fixed_mats: 
			If training, means feature matrice of onehot PEP matrice.
				shape = [BATCH_SIZE, NUM_PEPGROUP*PEP_HEIGHT*PEP_WIDTH] for NUM_PEPGROUP peps in one line
				or [BATCH_SIZE, NUM_PEPGROUP, PEP_HEIGHT*PEP_WIDTH] for them in NUM_PEPGROUP lines.
			If utilizing, means normal matrice generated by 'gmm_args' 
				shape = [BATCH_SIZE, NUM_PEPGROUP*MUTR_HEIGHT*MUTR_WIDTH]
	return:
		If training,
			mutrs: Means mutational R matrice, shape = [BATCH_SIZE, NUM_PEPGROUP*MUTR_HEIGHT*MUTR_WIDTH]
			new_peps: Peps generated by model, shape: as same as 'fixed_mats'
			ics: IC values generated by model, shape = [BATCH_SIZE, NUM_PEPGROUP]
		If utilizing,
			new_peps
			ics
	"""
	fixed_mhc = encode_onehot_mhc_by_rnn(onehot_mhc, MHC_HIDDEN_SIZE, regularizer)
	if regularizer != None:
		mutrs = run_convRNN(fixed_mhc, fixed_mats, regularizer)
		new_peps = run_multiRNN(fixed_mhc, mutrs, regularizer)
	else:
		new_peps = run_multiRNN(fixed_mhc, fixed_mats, None)
	ics = calc_ic(fixed_mhc, new_peps, regularizer)
	
	if regularizer != None:
		return mutrs, new_peps, ics
	return new_peps, ics